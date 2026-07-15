#!/usr/bin/env python3
import argparse
import csv
import html
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown


MP_BASE = "https://mp.weixin.qq.com"
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
    stat_keys = [
        "read_num",
        "old_like_num",
        "like_num",
        "share_num",
        "comment_num",
        "total_comment_count_contains_reply",
        "reprint_num",
        "moment_like_num",
        "appmsgid",
        "itemidx",
        "is_deleted",
        "copyright_type",
        "copyright_status",
        "copy_type",
        "copy_appmsg_id",
    ]
    stats = {key: record.get(key) for key in stat_keys if key in record}
    publish = record.get("_publish") or {}
    for key in ["msgid", "publish_type", "sent_status", "sent_result", "new_publish"]:
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
}


def field_label(key: str) -> str:
    if key.startswith("stat_"):
        key = key.removeprefix("stat_")
    return FIELD_LABELS.get(key, key)


def front_matter(article: Article) -> str:
    fields: dict[str, Any] = {
        "title": article.title,
        "account": article.account_name,
        "author": article.author,
        "publish_time": article.publish_time,
        "url": article.url,
    }
    fields.update({f"stat_{key}": value for key, value in article.stats.items()})
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        value = "" if value is None else str(value).replace("\n", " ").strip()
        lines.append(f"{field_label(key)}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


def write_outputs(articles: list[Article], output_dir: Path) -> None:
    article_dir = output_dir / "articles"
    article_dir.mkdir(parents=True, exist_ok=True)

    used: set[str] = set()
    rows: list[dict[str, Any]] = []
    all_stat_keys = sorted({key for article in articles for key in article.stats})

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
