import { API_BASE, loadSession } from "./api.js";
import { showAuth } from "./auth.js";

export function showRoadmap() {
  const { user } = loadSession();
  if (!user) return showAuth();

  view.innerHTML = `
    <h2 class="title">Choose a Skill Track</h2>
    <select id="skill" class="input">
      <option>Web Development</option>
      <option>DSA in Java</option>
      <option>Data Science</option>
    </select>
    <button class="btn neon-btn" id="btn_fetch">Load Roadmap</button>
    <button class="btn neon-btn" id="btn_ai_plan" style="margin-left:8px;">Generate My Weekly Plan (AI)</button>
    <div id="roadmap_out" class="stack"></div>
    <div id="ai_plan" class="card glass" style="display:none;"></div>
  `;

  document.getElementById("btn_fetch").onclick = fetchRoadmap;
  document.getElementById("btn_ai_plan").onclick = generatePlan;
}

async function fetchRoadmap() {
  const skillVal = document.getElementById("skill").value;
  const r = await fetch(`${API_BASE}/roadmap/${encodeURIComponent(skillVal)}`);
  const data = await r.json();
  if (!r.ok) {
    roadmap_out.innerHTML = `<div class="card glass">No roadmap found.</div>`;
    return;
  }
  roadmap_out.innerHTML = data.weeks.map(w => `
    <div class="card glass">
      <b>Week ${w.week_number}</b> — ${w.topics.join(", ")}<br>
      <small>${w.video_links.map(v=>`<a href="${v}" target="_blank">${v}</a>`).join(" | ")}</small>
    </div>
  `).join("");
}

async function generatePlan() {
  const { user } = loadSession();
  const skillVal = document.getElementById("skill").value;
  const box = document.getElementById("ai_plan");
  box.style.display = "block";
  box.innerHTML = "⏳ Creating your 7-day plan…";

  const r = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      user_id: user.id,
      message: `Create a concise 7-day study plan for ${skillVal}. Include daily tasks, 1-2 video topics per day, and a quick revision tip.`
    })
  });
  const data = await r.json();
  box.innerHTML = `<b>Weekly Plan</b><br>` + (data.response || "AI unavailable").replace(/\n/g, "<br>");
}
