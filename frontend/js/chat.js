import { API_BASE, loadSession } from "./api.js";
import { showAuth } from "./auth.js";

export function showChat() {
  const { user } = loadSession();
  if (!user) return showAuth();

  view.innerHTML = `
    <h2 class="title">AI Mentor</h2>
    <div class="card glass">
      <textarea id="msg" class="input" placeholder="Ask something like: “What should I study next?”" rows="3"></textarea>
      <button class="btn neon-btn" id="btn_send">Send</button>
      <div id="chat_out" class="stack"></div>
    </div>
  `;
  document.getElementById("btn_send").onclick = sendMessage;
}

async function sendMessage() {
  const { user } = loadSession();
  const msgEl = document.getElementById("msg");
  const chatOut = document.getElementById("chat_out");
  const message = msgEl.value.trim();
  if (!message) return;

  chatOut.innerHTML = `<div class="card glass user"><b>You:</b> ${message}</div>` + chatOut.innerHTML;
  msgEl.value = "";

  try {
    const r = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: user.id, message })
    });
    const data = await r.json();
    const reply = data?.response || "⚠️ Mentor could not reply. Check API key.";
    chatOut.innerHTML = `<div class="card glass bot"><b>Mentor:</b> ${reply}</div>` + chatOut.innerHTML;
  } catch {
    chatOut.innerHTML = `<div class="card glass bot"><b>Mentor:</b> ❗ Network Error</div>` + chatOut.innerHTML;
  }
}
