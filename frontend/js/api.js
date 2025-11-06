// js/api.js

export const API_BASE = "http://127.0.0.1:8000";

export function saveSession(token, user) {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
}

export function loadSession() {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "null");
  return { token, user };
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  location.reload();
}
