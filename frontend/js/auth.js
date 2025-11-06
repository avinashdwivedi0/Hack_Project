import { API_BASE, saveSession } from "./api.js";
import { showRoadmap } from "./roadmap.js";

export function showAuth() {
  view.innerHTML = `
    <div class="card glass neon">
      <h2>Sign Up</h2>
      <input id="su_name" class="input" placeholder="Full Name">
      <input id="su_email" class="input" placeholder="Email">
      <input id="su_pass" type="password" class="input" placeholder="Password">
      <button class="btn neon-btn" id="btn_register">Create Account</button>
    </div>

    <div class="card glass neon">
      <h2>Login</h2>
      <input id="li_email" class="input" placeholder="Email">
      <input id="li_pass" type="password" class="input" placeholder="Password">
      <button class="btn neon-btn" id="btn_login">Login</button>
    </div>
  `;
  document.getElementById("btn_register").onclick = registerUser;
  document.getElementById("btn_login").onclick = loginUser;
}

async function registerUser() {
  const name = su_name.value.trim();
  const email = su_email.value.trim();
  const password = su_pass.value;

  const r = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name, email, password })
  });

  if (!r.ok) return alert("Registration failed ❌");
  alert("Registered ✅ Logging in…");
  await loginUser(email, password);
}

async function loginUser(emailOverride, passOverride) {
  const email = emailOverride ?? li_email.value.trim();
  const password = passOverride ?? li_pass.value;

  const r = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email, password })
  });
  const data = await r.json();
  if (!r.ok) return alert(data.detail || "Login failed ❌");

  // backend sends access_token
  saveSession(data.access_token, data.user);
  showRoadmap();
}
