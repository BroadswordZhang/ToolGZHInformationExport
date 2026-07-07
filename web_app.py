#!/usr/bin/env python3
import csv
import json
import re
import sys
import threading
import time
import uuid
import webbrowser
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from wechat_public_account_exporter import (
    article_from_publish_record,
    fetch_article,
    list_articles,
    list_publish_records,
    make_session,
    search_account,
    fetch_stats,
    write_outputs,
)


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return str(Path(base_path) / relative_path)


app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static"),
)
JOBS: dict[str, dict[str, Any]] = {}
JOBS_LOCK = threading.Lock()
DEFAULT_ACCOUNT = "张大刀修炼手册"
DEFAULT_FAKEID = "MzU3ODk2Njc5Mg=="
OUTPUT_ROOT = Path.cwd().resolve()
ALLOWED_SOURCES = {"publish", "appmsg"}


def redact_sensitive(value: Any) -> str:
    text = str(value)
    text = re.sub(r"(token=)\d+", r"\1***", text, flags=re.I)
    text = re.sub(r"([?&]token=)\d+", r"\1***", text, flags=re.I)
    text = re.sub(r"(\btoken\b[\"'=:\s]+)\d+", r"\1***", text, flags=re.I)
    text = re.sub(r"(Cookie\s*:?\s*)[^\n\r]+", r"\1***", text, flags=re.I)
    return text


def parse_positive_float(value: Any, field_name: str, default: float, minimum: float, maximum: float) -> float:
    if value in (None, ""):
        return default
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} 必须是数字") from error
    if number < minimum or number > maximum:
        raise ValueError(f"{field_name} 必须在 {minimum} 到 {maximum} 之间")
    return number


def parse_optional_limit(value: Any) -> int | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        limit = int(raw)
    except ValueError as error:
        raise ValueError("最多提取必须是整数") from error
    if limit < 1 or limit > 1000:
        raise ValueError("最多提取必须在 1 到 1000 之间")
    return limit


def resolve_output_dir(value: Any) -> str:
    raw = (str(value or "web_output").strip() or "web_output").replace("\\", "/")
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("输出目录必须是当前项目下的相对路径")
    resolved = (OUTPUT_ROOT / path).resolve()
    try:
        resolved.relative_to(OUTPUT_ROOT)
    except ValueError as error:
        raise ValueError("输出目录必须位于当前项目目录内") from error
    return str(path)


def update_job(job_id: str, **updates: Any) -> None:
    with JOBS_LOCK:
        job = JOBS[job_id]
        job.update(updates)


def add_log(job_id: str, message: str) -> None:
    with JOBS_LOCK:
        job = JOBS[job_id]
        job.setdefault("logs", []).append(f"{time.strftime('%H:%M:%S')} {message}")
        job["logs"] = job["logs"][-200:]


def public_job(job_id: str) -> dict[str, Any]:
    with JOBS_LOCK:
        job = dict(JOBS[job_id])
    job.pop("cookie", None)
    return job


def load_summary(output_dir: str) -> list[dict[str, str]]:
    path = Path(output_dir) / "summary.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def run_export_job(job_id: str, params: dict[str, Any]) -> None:
    try:
        cookie = params["cookie"]
        token = params["token"]
        account_name = params["account"]
        fakeid = params.get("fakeid", "")
        output_dir = params["output"]
        sleep_seconds = float(params["sleep"])
        limit = params.get("limit")
        source = params["source"]

        session = make_session(cookie)
        if fakeid:
            account = {"nickname": account_name, "fakeid": fakeid}
        else:
            add_log(job_id, "正在按公众号名称搜索账号")
            account = search_account(session, account_name, token)
        fakeid = account.get("fakeid")
        if not fakeid:
            raise RuntimeError("没有获取到公众号 fakeid")

        add_log(job_id, f"匹配账号：{account.get('nickname')} fakeid={fakeid}")
        articles = []

        if source == "publish":
            add_log(job_id, "正在读取后台发表记录")
            items = list_publish_records(session, token, sleep_seconds, limit)
            update_job(job_id, total=len(items), done=0)
            for index, item in enumerate(items, 1):
                base_article = article_from_publish_record(item, account_name)
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
                    except Exception as error:
                        article = base_article
                        article.content_md = f"> Fetch failed: {error}"
                else:
                    article = base_article
                articles.append(article)
                update_job(job_id, done=index)
                add_log(job_id, f"已提取：{article.title}")
                time.sleep(sleep_seconds)
        else:
            add_log(job_id, "正在读取旧版文章列表")
            items = list_articles(session, fakeid, token, sleep_seconds, limit)
            update_job(job_id, total=len(items), done=0)
            for index, item in enumerate(items, 1):
                url = item.get("link")
                if not url:
                    continue
                article = fetch_article(session, url)
                article.digest = item.get("digest") or ""
                article.raw = item
                article.stats = fetch_stats(session, article)
                articles.append(article)
                update_job(job_id, done=index)
                add_log(job_id, f"已提取：{article.title}")
                time.sleep(sleep_seconds)

        write_outputs(articles, Path(output_dir))
        rows = load_summary(output_dir)
        update_job(
            job_id,
            status="completed",
            done=len(articles),
            total=len(articles),
            output=output_dir,
            preview=rows[:20],
        )
        add_log(job_id, f"导出完成：{output_dir}")
    except Exception as error:
        safe_error = redact_sensitive(error)
        update_job(job_id, status="failed", error=safe_error)
        add_log(job_id, f"导出失败：{safe_error}")


@app.get("/")
def index():
    return render_template(
        "index.html",
        default_account=DEFAULT_ACCOUNT,
        default_fakeid=DEFAULT_FAKEID,
    )


@app.post("/api/jobs")
def create_job():
    payload = request.get_json(silent=True) or {}
    cookie = (payload.get("cookie") or "").strip()
    token = (payload.get("token") or "").strip()
    if not cookie or not token:
        return jsonify({"error": "Cookie 和 token 必填"}), 400
    if not token.isdigit():
        return jsonify({"error": "token 必须是后台 URL 中的数字"}), 400

    try:
        source = payload.get("source") or "publish"
        if source not in ALLOWED_SOURCES:
            raise ValueError("数据来源无效")
        output = resolve_output_dir(payload.get("output"))
        sleep_seconds = parse_positive_float(payload.get("sleep"), "请求间隔", 5, 1, 120)
        limit = parse_optional_limit(payload.get("limit"))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    job_id = uuid.uuid4().hex
    params = {
        "account": (payload.get("account") or DEFAULT_ACCOUNT).strip(),
        "fakeid": (payload.get("fakeid") or "").strip(),
        "cookie": cookie,
        "token": token,
        "output": output,
        "sleep": sleep_seconds,
        "limit": limit,
        "source": source,
    }
    with JOBS_LOCK:
        JOBS[job_id] = {
            "id": job_id,
            "status": "running",
            "created_at": time.time(),
            "total": 0,
            "done": 0,
            "output": output,
            "logs": [],
            "preview": [],
        }
    thread = threading.Thread(target=run_export_job, args=(job_id, params), daemon=True)
    thread.start()
    return jsonify({"job_id": job_id})


@app.get("/api/jobs/<job_id>")
def get_job(job_id: str):
    if job_id not in JOBS:
        return jsonify({"error": "任务不存在"}), 404
    return jsonify(public_job(job_id))


@app.get("/api/jobs/<job_id>/summary")
def get_summary(job_id: str):
    if job_id not in JOBS:
        return jsonify({"error": "任务不存在"}), 404
    output_dir = public_job(job_id).get("output") or "web_output"
    return jsonify({"rows": load_summary(output_dir)})


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:7860")).start()
    app.run(host="127.0.0.1", port=7860, debug=False)
