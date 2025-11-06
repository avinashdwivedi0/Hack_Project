import { API_BASE, loadSession } from "./api.js";
import { showAuth } from "./auth.js";

const view = window.view;  // ✅ Fix: access main view container

export function showQuiz() {
  const { user } = loadSession();
  if (!user) return showAuth();

  view.innerHTML = `
    <h2 class="title">Skill Quiz</h2>
    <select id="q_skill" class="input">
      <option>Web Development</option>
      <option>DSA in Java</option>
      <option>Data Science</option>
    </select>
    <button class="btn neon-btn" id="btn_qfetch">Start Quiz</button>
    <button class="btn" id="btn_new" style="margin-left:8px;">New AI Quiz</button>
    <div id="q_box" class="stack"></div>
  `;

  document.getElementById("btn_qfetch").onclick = () => loadQuiz(false);
  document.getElementById("btn_new").onclick = () => loadQuiz(true);
}

async function loadQuiz(forceAI = false) {
  const skill = document.getElementById("q_skill").value;
  const qb = document.getElementById("q_box");
  qb.innerHTML = "";

  if (!forceAI) {
    const r = await fetch(`${API_BASE}/quiz/${encodeURIComponent(skill)}`);
    if (r.ok) {
      const data = await r.json();
      return renderQuiz(data);
    }
  }

  qb.innerHTML = `<div class="card glass">⏳ Generating quiz… please wait 5–10 seconds</div>`;

  const r2 = await fetch(`${API_BASE}/quiz`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ skill, count: 10 })
  });

  if (!r2.ok) {
    const err = await r2.json().catch(() => ({detail:"Quiz generation failed"}));
    qb.innerHTML = `<div class="card glass">❌ ${err.detail || "Quiz generation failed"}</div>`;
    return;
  }

  const data2 = await r2.json();
  renderQuiz(data2);
}

function renderQuiz(data) {
  const qb = document.getElementById("q_box");
  qb.innerHTML = data.questions.map((q, qi) => `
    <div class="card glass">
      <b>Q${qi + 1}.</b> ${q.question}
      ${q.options.map((op, oi) => `
        <label class="row" style="display:block;margin:6px 0;">
          <input type="radio" name="q${qi}" value="${oi}"> ${op}
        </label>
      `).join("")}
    </div>
  `).join("");

  qb.innerHTML += `
    <button class="btn neon-btn" id="btn_submit">Submit</button>
    <div id="score" class="badge"></div>
  `;

  document.getElementById("btn_submit").onclick = () => submitQuiz(data);
}

async function submitQuiz(data) {
  const { user } = loadSession();
  const answers = data.questions.map((_, qi) => {
    const el = document.querySelector(`input[name="q${qi}"]:checked`);
    return el ? parseInt(el.value, 10) : -1;
  });

  const res = await fetch(`${API_BASE}/quiz/submit`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ user_id: user.id, skill_id: data.skill_id, answers })
  });

  const result = await res.json();
  document.getElementById("score").textContent =
    `Score: ${result.correct}/${result.total} (${result.score}%) • +${result.xp_gain} XP • Level ${result.level}`;
}
