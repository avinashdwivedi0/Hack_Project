import { API_BASE, loadSession } from "./api.js";
import { showAuth } from "./auth.js";

export function showProgress() {
  const { user } = loadSession();
  if (!user) return showAuth();

  view.innerHTML = `
    <h2 class="title">Your Progress</h2>
    <button class="btn neon-btn" id="btn_load">Load Progress</button>
    <div id="prog" class="stack"></div>
  `;
  document.getElementById("btn_load").onclick = loadProgress;
}

async function loadProgress() {
  const { user } = loadSession();
  const r = await fetch(`${API_BASE}/progress/${user.id}`);
  const data = await r.json();
  const prog = document.getElementById("prog");

  if (!r.ok || !data.items.length) {
    prog.innerHTML = `<div class="card glass">No progress yet. Complete quizzes to track progress.</div>`;
    return;
  }

  prog.innerHTML = data.items.map(p => `
    <div class="card glass">
      <b>${p.skill_id}</b>
      <div>Completed: ${p.completed_percentage}%</div>
      <div>Streak: 🔥 ${p.streak_days} days</div>
      <div>XP: ⭐ ${p.xp || 0} &nbsp; | &nbsp; Level: 🎯 ${p.level || 1}</div>
    </div>
  `).join("");
}
