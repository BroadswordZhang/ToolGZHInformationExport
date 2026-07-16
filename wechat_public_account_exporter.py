#!/usr/bin/env python3
import argparse
import csv
import html
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown


MP_BASE = "https://mp.weixin.qq.com"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    ),
    "Referer": "https://mp.weixin.qq.com/",
}


@dataclass
class Article:
    title: str
    url: str
    author: str = ""
    account_name: str = ""
    publish_time: str = ""
    digest: str = ""
    content_md: str = ""
    content_html: str = ""
    params: dict[str, str] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    analysis: dict[str, Any] = field(default_factory=dict)


def make_session(cookie: str | None = None) -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.headers.update(DEFAULT_HEADERS)
    if cookie:
        session.headers.update({"Cookie": cookie})
    return session


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    attempts: int = 3,
    sleep_seconds: float = 2.0,
    **kwargs: Any,
) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            last_error = error
            if attempt == attempts:
                break
            time.sleep(sleep_seconds * attempt)
    assert last_error is not None
    raise last_error


def get_json(session: requests.Session, url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = request_with_retry(session, "GET", url, params=params, timeout=45)
    text = response.text.strip()
    if text.startswith("{"):
        return response.json()
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise RuntimeError(f"Response is not JSON: {text[:200]}")
    return json.loads(match.group(0))


def extract_token_from_cookie(cookie: str) -> str:
    match = re.search(r"(?:^|;\s*)token=(\d+)", cookie)
    return match.group(1) if match else ""


def search_account(session: requests.Session, account_name: str, token: str) -> dict[str, Any]:
    data = get_json(
        session,
        f"{MP_BASE}/cgi-bin/searchbiz",
        {
            "action": "search_biz",
            "begin": 0,
            "count": 5,
            "query": account_name,
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
        },
    )
    accounts = data.get("list") or []
    if not accounts:
        raise RuntimeError(f"No account matched: {account_name}")
    exact = next((item for item in accounts if item.get("nickname") == account_name), None)
    return exact or accounts[0]


def list_articles(
    session: requests.Session,
    fakeid: str,
    token: str,
    sleep_seconds: float,
    limit: int | None,
) -> list[dict[str, Any]]:
    articles: list[dict[str, Any]] = []
    begin = 0
    count = 5
    while True:
        data = get_json(
            session,
            f"{MP_BASE}/cgi-bin/appmsg",
            {
                "action": "list_ex",
                "begin": begin,
                "count": count,
                "fakeid": fakeid,
                "type": 9,
                "query": "",
                "token": token,
                "lang": "zh_CN",
                "f": "json",
                "ajax": 1,
            },
        )
        base_resp = data.get("base_resp") or {}
        if base_resp.get("ret") not in (None, 0):
            raise RuntimeError(f"Article list API error: ret={base_resp.get('ret')} err_msg={base_resp.get('err_msg')}")
        batch = data.get("app_msg_list") or []
        if not batch:
            break
        articles.extend(batch)
        if limit and len(articles) >= limit:
            return articles[:limit]
        total = int(data.get("app_msg_cnt") or 0)
        begin += count
        if begin >= total:
            break
        time.sleep(sleep_seconds)
    return articles


def extract_publish_page(html_text: str) -> dict[str, Any]:
    match = re.search(r"publish_page\s*=\s*(\{.*?\});\s*\n\s*isPublishPageNoEncode", html_text, flags=re.S)
    if not match:
        raise RuntimeError("Cannot find publish_page data in publish record page.")
    return json.loads(match.group(1))


def parse_publish_info(value: str) -> dict[str, Any]:
    return json.loads(html.unescape(value))


def flatten_publish_records(page: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for publish_item in page.get("publish_list") or []:
        publish_info = parse_publish_info(publish_item.get("publish_info") or "{}")
        parent = {
            "publish_type": publish_item.get("publish_type"),
            "msgid": publish_info.get("msgid"),
            "sent_info": publish_info.get("sent_info") or {},
            "sent_status": publish_info.get("sent_status") or {},
            "sent_result": publish_info.get("sent_result") or {},
            "copy_type": publish_info.get("copy_type"),
            "copy_appmsg_id": publish_info.get("copy_appmsg_id"),
            "new_publish": publish_info.get("new_publish"),
        }
        for appmsg in publish_info.get("appmsg_info") or []:
            record = dict(appmsg)
            record["_publish"] = parent
            records.append(record)
    return records


def list_publish_records(
    session: requests.Session,
    token: str,
    sleep_seconds: float,
    limit: int | None,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    begin = 0
    count = 10
    total = None
    while True:
        response = request_with_retry(
            session,
            "GET",
            f"{MP_BASE}/cgi-bin/appmsgpublish",
            params={
                "sub": "list",
                "begin": begin,
                "count": count,
                "token": token,
                "lang": "zh_CN",
            },
            timeout=60,
        )
        page = extract_publish_page(response.text)
        if total is None:
            total = int(page.get("total_count") or 0)
        batch = flatten_publish_records(page)
        if not batch:
            break
        records.extend(batch)
        if limit and len(records) >= limit:
            return records[:limit]
        begin += count
        if total and begin >= total:
            break
        time.sleep(sleep_seconds)
    return records


def first_group(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, flags=re.S)
    if not match:
        return default
    value = match.group(1)
    return html.unescape(value).strip().strip('"').strip("'")


def parse_url_params(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    params = {key: values[0] for key, values in parse_qs(parsed.query).items() if values}
    if "__biz" not in params:
        biz = first_group(r"var\s+biz\s*=\s*['\"]([^'\"]+)", url)
        if biz:
            params["__biz"] = biz
    return params


def parse_article_page(url: str, text: str) -> Article:
    soup = BeautifulSoup(text, "html.parser")
    content = soup.select_one("#js_content")
    title_node = soup.select_one("#activity-name")
    author_node = soup.select_one("#js_name")

    title = title_node.get_text(" ", strip=True) if title_node else ""
    author = author_node.get_text(" ", strip=True) if author_node else ""
    account_name = first_group(r"var\s+nickname\s*=\s*['\"]([^'\"]*)", text)
    publish_time = first_group(r"var\s+ct\s*=\s*['\"]?(\d+)", text)
    if publish_time:
        publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(publish_time)))

    content_html = str(content) if content else ""
    content_md = html_to_markdown(content_html, heading_style="ATX").strip() if content_html else ""

    params = parse_url_params(url)
    for key, pattern in {
        "__biz": r"var\s+biz\s*=\s*['\"]([^'\"]+)",
        "mid": r"var\s+mid\s*=\s*['\"]?([^'\";]+)",
        "idx": r"var\s+idx\s*=\s*['\"]?([^'\";]+)",
        "sn": r"var\s+sn\s*=\s*['\"]([^'\"]+)",
        "appmsg_token": r"window\.appmsg_token\s*=\s*['\"]([^'\"]+)",
    }.items():
        if key not in params:
            value = first_group(pattern, text)
            if value:
                params[key] = value

    return Article(
        title=title or params.get("title", "untitled"),
        url=url,
        author=author,
        account_name=account_name,
        publish_time=publish_time,
        content_md=content_md,
        content_html=content_html,
        params=params,
    )


def fetch_article(session: requests.Session, url: str) -> Article:
    response = request_with_retry(session, "GET", url, timeout=60)
    response.encoding = response.apparent_encoding or "utf-8"
    return parse_article_page(response.url, response.text)

def extract_inline_json(text: str, variable_name: str) -> Any:
    match = re.search(rf"{re.escape(variable_name)}\s*:\s*", text)
    if not match:
        raise RuntimeError(f"Missing {variable_name} in analysis page.")
    start = match.end()
    while start < len(text) and text[start].isspace():
        start += 1
    try:
        value, _ = json.JSONDecoder().raw_decode(text[start:])
    except ValueError as error:
        raise RuntimeError(f"Invalid {variable_name} in analysis page.") from error
    return value


def fetch_article_analysis(
    session: requests.Session,
    article: Article,
    token: str,
) -> dict[str, Any]:
    appmsgid = article.stats.get("appmsgid")
    itemidx = article.stats.get("itemidx")
    publish_date = article.publish_time[:10] if article.publish_time else ""
    if not appmsgid or not itemidx or not publish_date:
        return {"_error": "missing appmsgid/itemidx/publish_date"}
    try:
        response = request_with_retry(
            session,
            "GET",
            f"{MP_BASE}/misc/appmsganalysis",
            params={
                "action": "detailpage",
                "msgid": f"{appmsgid}_{itemidx}",
                "publish_date": publish_date,
                "type": "int",
                "pageVersion": "1",
                "token": token,
                "lang": "zh_CN",
            },
            timeout=60,
        )
        article_data = extract_inline_json(response.text, "articleData") or {}
        summary_data = extract_inline_json(response.text, "articleSummaryData") or {}
        try:
            detail_data = extract_inline_json(response.text, "detailData") or {}
        except RuntimeError:
            detail_data = {}
    except requests.RequestException:
        return {"_error": "analysis request failed"}
    except RuntimeError:
        return {"_error": "analysis page parsing failed"}
    analysis: dict[str, Any] = {}
    for key, value in (article_data.get("article_data_new") or {}).items():
        if value not in (None, ""):
            analysis[f"article_{key}"] = value
    for key, value in (article_data.get("subs_transform") or {}).items():
        if value not in (None, ""):
            analysis[f"transform_{key}"] = value
    analysis["daily_detail"] = summary_data.get("list") or []
    analysis["jump_stat"] = article_data.get("article_jump_stat") or []
    analysis["audio_listen"] = article_data.get("article_audio_listen_list") or []
    analysis["profile_genders"] = detail_data.get("genders") or []
    analysis["profile_ages"] = detail_data.get("ages") or []
    analysis["profile_regions"] = detail_data.get("regions") or []
    return analysis


def article_from_publish_record(record: dict[str, Any], account_name: str) -> Article:
    sent_info = (record.get("_publish") or {}).get("sent_info") or {}
    publish_time = ""
    if sent_info.get("time"):
        publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(sent_info["time"])))
    article = Article(
        title=record.get("title") or "untitled",
        url=record.get("content_url") or "",
        account_name=account_name,
        publish_time=publish_time,
        digest=record.get("digest") or "",
        raw=record,
    )
    article.stats = extract_publish_stats(record)
    return article


def extract_publish_stats(record: dict[str, Any]) -> dict[str, Any]:
    stats: dict[str, Any] = {}
    excluded_keys = {"title", "content_url", "digest", "author"}
    for key, value in record.items():
        if key.startswith("_") or key in excluded_keys:
            continue
        if value not in (None, ""):
            stats[key] = value

    publish = record.get("_publish") or {}
    for key in [
        "msgid",
        "publish_type",
        "sent_status",
        "sent_result",
        "new_publish",
        "copy_type",
        "copy_appmsg_id",
    ]:
        if key in publish:
            stats[f"publish_{key}"] = publish[key]
    return stats


def fetch_stats(session: requests.Session, article: Article) -> dict[str, Any]:
    params = article.params
    required = ["__biz", "mid", "idx", "sn"]
    if not all(params.get(key) for key in required):
        return {"_error": "missing __biz/mid/idx/sn"}

    query = {
        "__biz": params.get("__biz"),
        "mid": params.get("mid"),
        "idx": params.get("idx"),
        "sn": params.get("sn"),
        "appmsg_type": 9,
        "f": "json",
        "r": int(time.time()),
        "is_need_ad": 0,
        "comment_id": "",
        "is_need_reward": 0,
        "both_ad": 0,
        "reward_uin_count": 0,
        "send_time": "",
    }
    for optional_key in ["key", "pass_ticket", "appmsg_token", "uin", "devicetype", "version"]:
        if params.get(optional_key):
            query[optional_key] = params[optional_key]

    response = request_with_retry(session, "GET", f"{MP_BASE}/mp/getappmsgext", params=query, timeout=45)
    if response.status_code != 200:
        return {"_error": f"status {response.status_code}"}
    try:
        data = response.json()
    except ValueError:
        return {"_error": response.text[:200]}
    stats = data.get("appmsgstat") or {}
    if not stats:
        stats = {"_raw": data}
    return stats


def safe_filename(value: str, fallback: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\r\n\t]+", " ", value).strip()
    value = re.sub(r"\s+", " ", value)
    return (value[:100] or fallback).strip()


FIELD_LABELS = {
    "index": "序号",
    "title": "标题",
    "account": "公众号名称",
    "author": "作者",
    "publish_time": "发布时间",
    "url": "原文链接",
    "file": "Markdown文件",
    "read_num": "阅读量",
    "old_like_num": "点赞数",
    "like_num": "喜欢数",
    "share_num": "分享量",
    "comment_num": "留言数",
    "total_comment_count_contains_reply": "留言含回复数",
    "reprint_num": "转载量",
    "moment_like_num": "朋友圈点赞数",
    "appmsgid": "文章ID",
    "itemidx": "图文序号",
    "is_deleted": "是否已删除",
    "copyright_type": "版权类型",
    "copyright_status": "版权状态",
    "publish_msgid": "发布消息ID",
    "publish_publish_type": "发布类型",
    "publish_sent_status": "发送状态",
    "publish_sent_result": "发布结果",
    "publish_new_publish": "是否新发布",
    "read_count": "接口阅读量",
    "like_count": "接口点赞数",
    "old_like_count": "接口旧点赞数",
    "share_count": "接口分享量",
    "comment_count": "接口留言数",
    "_error": "统计错误",
    "_raw": "原始统计",
    "ad_info": "文章详情_广告信息",
    "appmsg_album_info": "文章详情_文章合集信息",
    "appmsg_like_type": "文章详情_互动类型",
    "appmsg_modified": "文章详情_是否修改",
    "audio_in_appmsg": "文章详情_文章音频信息",
    "can_delete_status": "文章详情_可删除状态",
    "can_location_page_show": "文章详情_可显示位置页",
    "can_modify": "文章详情_可修改状态",
    "claim_source": "文章详情_来源声明信息",
    "claim_source_type": "文章详情_来源声明类型",
    "comment_id": "文章详情_留言ID",
    "cover": "文章详情_封面图片",
    "delete_nickname": "文章详情_删除操作人",
    "delete_time": "文章详情_删除时间",
    "disable_recommend": "文章详情_是否禁止推荐",
    "is_comment_enable": "文章详情_是否开启留言",
    "is_cooling_article": "文章详情_是否处于冷却状态",
    "is_forced_reprint": "文章详情_是否强制转载",
    "is_from_transfer": "文章详情_是否来自转移",
    "is_pay_subscribe": "文章详情_是否付费订阅",
    "is_rumor_refutation": "文章详情_是否辟谣文章",
    "is_segment_comment_enable": "文章详情_是否开启精选留言",
    "item_show_type": "文章详情_图文展示类型",
    "line_info": "文章详情_发布线路信息",
    "location_page_show": "文章详情_位置页展示",
    "modify_detail_wording": "文章详情_修改详情说明",
    "modify_status": "文章详情_修改状态",
    "modify_wording": "文章详情_修改提示",
    "multi_picture_cover": "文章详情_是否多图封面",
    "open_fansmsg": "文章详情_是否开启粉丝留言",
    "pic_cdn_url_16_9": "文章详情_16比9封面地址",
    "pic_cdn_url_1_1": "文章详情_1比1封面地址",
    "pic_cdn_url_235_1": "文章详情_2.35比1封面地址",
    "public_tag_info": "文章详情_公开标签信息",
    "publish_copy_appmsg_id": "文章详情_发布复制文章ID",
    "publish_copy_type": "文章详情_发布复制类型",
    "reprint_source_title": "文章详情_转载来源标题",
    "reprint_source_url": "文章详情_转载来源链接",
    "segment_comment_id": "文章详情_精选留言ID",
    "share_imageinfo": "文章详情_分享图片信息",
    "share_type": "文章详情_分享类型",
    "smart_product": "文章详情_智能产品信息",
    "super_vote_id": "文章详情_超级投票ID",
    "vote_id": "文章详情_投票ID",
    "article_read_uv": "阅读人数",
    "article_avg_article_read_time": "平均阅读时长",
    "article_finished_read_pv_ratio": "完读率",
    "article_like_cnt": "点赞人数",
    "article_zaikan_cnt": "在看人数",
    "article_comment_cnt": "分析页留言数",
    "article_share_uv": "分享人数",
    "article_collection_uv": "收藏人数",
    "article_follow_after_read_uv": "阅读后关注人数",
    "article_listen_pv": "音频播放次数",
    "article_listen_uv": "音频播放人数",
    "article_praise_money": "赞赏金额",
    "transform_all_share_pv": "总分享次数",
    "transform_fans_share_pv": "粉丝分享次数",
    "transform_read_in_share_scene_pv": "分享场景阅读次数",
    "transform_read_pv": "分析页阅读次数",
    "transform_send_uv": "送达人数",
    "daily_detail": "按日来源明细",
    "jump_stat": "文章内跳转统计",
    "audio_listen": "音频明细",
    "profile_genders": "性别分布",
    "profile_ages": "年龄分布",
    "profile_regions": "地域分布",
}


def field_label(key: str) -> str:
    if key.startswith("stat_"):
        key = key.removeprefix("stat_")
    if key.startswith("analysis_"):
        key = key.removeprefix("analysis_")
        return f"文章分析_{FIELD_LABELS.get(key, key)}"
    return FIELD_LABELS.get(key, f"文章详情_{key}")


def front_matter(article: Article) -> str:
    fields: dict[str, Any] = {
        "title": article.title,
        "account": article.account_name,
        "author": article.author,
        "publish_time": article.publish_time,
        "url": article.url,
    }
    fields.update({f"stat_{key}": value for key, value in article.stats.items()})
    fields.update({f"analysis_{key}": value for key, value in article.analysis.items()})
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        value = "" if value is None else str(value).replace("\n", " ").strip()
        lines.append(f"{field_label(key)}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


def ensure_output_writable(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in ("summary.csv", "summary.json"):
        try:
            with (output_dir / filename).open("a", encoding="utf-8"):
                pass
        except OSError as error:
            raise RuntimeError(
                f"Cannot write {filename}. Close programs that opened it and retry."
            ) from error


def write_outputs(articles: list[Article], output_dir: Path) -> None:
    ensure_output_writable(output_dir)
    article_dir = output_dir / "articles"
    article_dir.mkdir(parents=True, exist_ok=True)

    used: set[str] = set()
    rows: list[dict[str, Any]] = []
    all_stat_keys = sorted({key for article in articles for key in article.stats})
    all_analysis_keys = sorted({key for article in articles for key in article.analysis})

    for index, article in enumerate(articles, 1):
        base = safe_filename(f"{index:04d} {article.title}", f"article-{index:04d}")
        filename = f"{base}.md"
        suffix = 2
        while filename in used:
            filename = f"{base}-{suffix}.md"
            suffix += 1
        used.add(filename)
        (article_dir / filename).write_text(
            f"{front_matter(article)}\n\n# {article.title}\n\n{article.content_md}\n",
            encoding="utf-8",
        )

        row = {
            field_label("index"): index,
            field_label("title"): article.title,
            field_label("account"): article.account_name,
            field_label("author"): article.author,
            field_label("publish_time"): article.publish_time,
            field_label("url"): article.url,
            field_label("file"): str((article_dir / filename).resolve()),
        }
        for key in all_stat_keys:
            value = article.stats.get(key, "")
            row[field_label(key)] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        for key in all_analysis_keys:
            value = article.analysis.get(key, "")
            row[field_label(f"analysis_{key}")] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        rows.append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    with (output_dir / "summary.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)


def read_urls(path: Path) -> list[str]:
    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def export_from_urls(args: argparse.Namespace) -> None:
    cookie = load_cookie(args)
    session = make_session(cookie)
    urls = read_urls(Path(args.input))
    if not urls:
        raise RuntimeError(f"No URLs found in {args.input}")
    articles = []
    for url in urls:
        article = fetch_article(session, url)
        if cookie:
            article.stats = fetch_stats(session, article)
        articles.append(article)
        print(f"Fetched: {article.title}")
        time.sleep(args.sleep)
    write_outputs(articles, Path(args.output))


def export_from_account(args: argparse.Namespace) -> None:
    cookie = load_cookie(args)
    token = args.token or extract_token_from_cookie(cookie or "")
    if not cookie or not token:
        raise RuntimeError("Account mode requires --cookie/--cookie-file and --token.")
    session = make_session(cookie)
    if args.fakeid:
        account = {"nickname": args.account, "fakeid": args.fakeid}
    else:
        account = search_account(session, args.account, token)
        if account.get("nickname") != args.account:
            raise RuntimeError(
                f"Account search returned {account.get('nickname')!r}, not {args.account!r}. "
                "Pass --fakeid to skip account search."
            )
    fakeid = account.get("fakeid")
    if not fakeid:
        raise RuntimeError(f"Matched account has no fakeid: {account}")
    print(f"Matched account: {account.get('nickname')} fakeid={fakeid}")
    articles = []
    if args.source == "publish":
        items = list_publish_records(session, token, args.sleep, args.limit)
        for item in items:
            base_article = article_from_publish_record(item, args.account)
            if base_article.url:
                try:
                    article = fetch_article(session, base_article.url)
                    if article.title == "untitled" and base_article.title != "untitled":
                        article.title = base_article.title
                    article.digest = base_article.digest
                    article.raw = item
                    article.stats = base_article.stats
                    if not article.publish_time:
                        article.publish_time = base_article.publish_time
                    if not article.account_name:
                        article.account_name = base_article.account_name
                except requests.RequestException as error:
                    article = base_article
                    article.content_md = f"> Fetch failed: {error}"
            else:
                article = base_article
            article.analysis = fetch_article_analysis(session, article, token)
            articles.append(article)
            print(f"Fetched: {article.title}")
            time.sleep(args.sleep)
    else:
        items = list_articles(session, fakeid, token, args.sleep, args.limit)
        for item in items:
            url = item.get("link")
            if not url:
                continue
            article = fetch_article(session, url)
            article.digest = item.get("digest") or ""
            article.raw = item
            article.stats = fetch_stats(session, article)
            if article.stats.get("appmsgid") and article.stats.get("itemidx"):
                article.analysis = fetch_article_analysis(session, article, token)
            articles.append(article)
            print(f"Fetched: {article.title}")
            time.sleep(args.sleep)
    write_outputs(articles, Path(args.output))


def show_account(args: argparse.Namespace) -> None:
    cookie = load_cookie(args)
    token = args.token or extract_token_from_cookie(cookie or "")
    if not cookie or not token:
        raise RuntimeError("Search mode requires --cookie/--cookie-file and --token.")
    account = search_account(make_session(cookie), args.account, token)
    print(f"nickname: {account.get('nickname', '')}")
    print(f"fakeid: {account.get('fakeid', '')}")
    print(json.dumps(account, ensure_ascii=False, indent=2))


def load_cookie(args: argparse.Namespace) -> str:
    if getattr(args, "cookie_file", ""):
        return Path(args.cookie_file).read_text(encoding="utf-8").strip()
    return getattr(args, "cookie", "") or ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Export WeChat public account articles to Markdown.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    account = subparsers.add_parser("account", help="Search an account and export its articles.")
    account.add_argument("--account", required=True, help="WeChat public account name.")
    account.add_argument("--fakeid", default="", help="Known account fakeid; skips account search when provided.")
    account.add_argument("--cookie", default="", help="Cookie copied from mp.weixin.qq.com.")
    account.add_argument("--cookie-file", default="", help="File containing Cookie copied from mp.weixin.qq.com.")
    account.add_argument("--token", default="", help="token parameter from mp.weixin.qq.com backend URL.")
    account.add_argument("--output", default="output", help="Output directory.")
    account.add_argument("--sleep", type=float, default=2.0, help="Delay between requests.")
    account.add_argument("--limit", type=int, default=0, help="Max articles to export; 0 means all.")
    account.add_argument(
        "--source",
        choices=["publish", "appmsg"],
        default="publish",
        help="publish reads backend publish records with stats; appmsg uses the older article-list API.",
    )
    account.set_defaults(func=export_from_account)

    search = subparsers.add_parser("search", help="Search an account and print its fakeid.")
    search.add_argument("--account", required=True, help="WeChat public account name.")
    search.add_argument("--cookie", default="", help="Cookie copied from mp.weixin.qq.com.")
    search.add_argument("--cookie-file", default="", help="File containing Cookie copied from mp.weixin.qq.com.")
    search.add_argument("--token", default="", help="token parameter from mp.weixin.qq.com backend URL.")
    search.set_defaults(func=show_account)

    urls = subparsers.add_parser("urls", help="Export articles from a URL list.")
    urls.add_argument("--input", default="article_urls.txt", help="Input file, one URL per line.")
    urls.add_argument("--cookie", default="", help="Optional Cookie for reading stats.")
    urls.add_argument("--cookie-file", default="", help="Optional file containing Cookie for reading stats.")
    urls.add_argument("--output", default="output", help="Output directory.")
    urls.add_argument("--sleep", type=float, default=1.0, help="Delay between requests.")
    urls.set_defaults(func=export_from_urls)

    args = parser.parse_args()
    if hasattr(args, "limit") and args.limit == 0:
        args.limit = None
    args.func(args)


if __name__ == "__main__":
    main()
