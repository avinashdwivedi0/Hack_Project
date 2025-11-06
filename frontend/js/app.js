// js/app.js

import { logout, loadSession } from "./api.js";
import { showAuth } from "./auth.js";
import { showRoadmap } from "./roadmap.js";
import { showQuiz } from "./quiz.js";
import { showProgress } from "./progress.js";
import { showChat } from "./chat.js";

// ✅ Ensure `view` is available globally
window.view = document.getElementById("view");

// ✅ Load correct page on refresh
window.onload = () => {
  const { user } = loadSession();
  if (user) showRoadmap();
  else showAuth();
};

// ✅ Navbar button handling
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const v = btn.dataset.view;

    switch (v) {
      case "auth":
        showAuth();
        break;
      case "roadmap":
        showRoadmap();
        break;
      case "quiz":
        showQuiz();
        break;
      case "progress":
        showProgress();
        break;
      case "chat":
        showChat();
        break;
      case "logout":
        logout();
        break;
    }
  });
});
