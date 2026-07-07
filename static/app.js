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
  statusPill.className = `pill ${status}`;
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
        <td>${escapeHtml(row.title || "")}</td>
        <td>${escapeHtml(row.read_num || "")}</td>
        <td>${escapeHtml(row.old_like_num || "")}</td>
        <td>${escapeHtml(row.like_num || "")}</td>
        <td>${escapeHtml(row.share_num || "")}</td>
        <td>${escapeHtml(row.total_comment_count_contains_reply || row.comment_num || "")}</td>
        <td>${escapeHtml(row.reprint_num || "")}</td>
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
  logs.textContent = (job.logs || []).join("\n");
  logs.scrollTop = logs.scrollHeight;

  const total = Number(job.total || 0);
  const done = Number(job.done || 0);
  progressBar.style.width = total > 0 ? `${Math.min(100, (done / total) * 100)}%` : "3%";

  if (job.preview) {
    renderRows(job.preview);
  }

  if (job.status === "completed" || job.status === "failed") {
    clearInterval(pollTimer);
    pollTimer = null;
    button.disabled = false;
    refreshSummary.disabled = job.status !== "completed";
    if (job.error) message.textContent = job.error;
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
