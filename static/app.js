const form = document.querySelector("#export-form");
const button = document.querySelector("#submit-button");
const message = document.querySelector("#form-message");
const statusPill = document.querySelector("#status-pill");
const progressBar = document.querySelector("#progress-bar");
const doneCount = document.querySelector("#done-count");
const totalCount = document.querySelector("#total-count");
const outputDir = document.querySelector("#output-dir");
const logs = document.querySelector("#logs");
const resultBody = document.querySelector("#result-body");
const refreshSummary = document.querySelector("#refresh-summary");

let currentJobId = null;
let pollTimer = null;

function formDataToPayload() {
  const data = new FormData(form);
  return Object.fromEntries(data.entries());
}

function setStatus(status) {
  const text = {
    idle: "未开始",
    running: "运行中",
    completed: "已完成",
    failed: "失败",
  }[status] || status;
  statusPill.textContent = text;
  statusPill.className = `status-text ${status}`;
}

function rowValue(row, ...keys) {
  for (const key of keys) {
    const value = row[key];
    if (value !== undefined && value !== null && value !== "") return value;
  }
  return "";
}

function renderRows(rows) {
  if (!rows || rows.length === 0) {
    resultBody.innerHTML = '<tr><td colspan="7" class="empty">暂无结果</td></tr>';
    return;
  }

  resultBody.innerHTML = rows
    .slice(0, 20)
    .map((row) => `
      <tr>
        <td class="title-cell">${escapeHtml(rowValue(row, "标题", "title"))}</td>
        <td><span class="num">${escapeHtml(rowValue(row, "阅读量", "read_num"))}</span></td>
        <td><span class="num">${escapeHtml(rowValue(row, "点赞数", "old_like_num"))}</span></td>
        <td><span class="num">${escapeHtml(rowValue(row, "喜欢数", "like_num"))}</span></td>
        <td><span class="num">${escapeHtml(rowValue(row, "分享量", "share_num"))}</span></td>
        <td><span class="num">${escapeHtml(rowValue(row, "留言含回复数", "留言数", "total_comment_count_contains_reply", "comment_num"))}</span></td>
        <td><span class="num">${escapeHtml(rowValue(row, "转载量", "reprint_num"))}</span></td>
      </tr>
    `)
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function pollJob() {
  if (!currentJobId) return;
  const response = await fetch(`/api/jobs/${currentJobId}`);
  const job = await response.json();
  if (!response.ok) {
    message.textContent = job.error || "任务状态读取失败";
    return;
  }

  setStatus(job.status);
  doneCount.textContent = job.done || 0;
  totalCount.textContent = job.total || 0;
  outputDir.textContent = job.output || "-";
  logs.textContent = (job.logs || []).join("\n") || "等待任务日志";
  logs.scrollTop = logs.scrollHeight;

  const total = Number(job.total || 0);
  const done = Number(job.done || 0);
  progressBar.style.width = total > 0 ? `${Math.min(100, (done / total) * 100)}%` : "4%";

  if (job.preview) {
    renderRows(job.preview);
  }

  if (job.status === "completed" || job.status === "failed") {
    clearInterval(pollTimer);
    pollTimer = null;
    button.disabled = false;
    refreshSummary.disabled = job.status !== "completed";
    message.textContent = job.status === "completed" ? "导出完成" : (job.error || "导出失败");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  refreshSummary.disabled = true;
  message.textContent = "任务创建中";
  setStatus("running");
  renderRows([]);

  const response = await fetch("/api/jobs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formDataToPayload()),
  });
  const data = await response.json();
  if (!response.ok) {
    button.disabled = false;
    setStatus("failed");
    message.textContent = data.error || "任务创建失败";
    return;
  }

  currentJobId = data.job_id;
  message.textContent = `任务已创建：${currentJobId}`;
  await pollJob();
  pollTimer = setInterval(pollJob, 1500);
});

refreshSummary.addEventListener("click", async () => {
  if (!currentJobId) return;
  const response = await fetch(`/api/jobs/${currentJobId}/summary`);
  const data = await response.json();
  renderRows(data.rows || []);
});
