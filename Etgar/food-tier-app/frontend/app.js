/*
 * Frontend integration layer.
 *
 * Wires the form in index.html to the FastAPI backend:
 *   POST {API_BASE}/api/food-tier   body: {"food": "<name>"}
 *   ->  {food, tier, explanation, source}
 *
 * Nginx (port 8080) only serves the static files — it does NOT proxy /api,
 * so the browser talks to the backend on port 8000 directly. CORS for
 * localhost:8080 / 127.0.0.1:8080 is whitelisted in backend/main.py.
 */

// Derive the API base from the page's host so the same build works for
// `http://localhost:8080` (dev) and `http://<ec2-ip>:8080` (deployed).
// `file://` (opening index.html from disk) falls back to localhost.
const API_BASE = (() => {
  const host = window.location.hostname || "localhost";
  const protocol =
    window.location.protocol === "https:" ? "https:" : "http:";
  return `${protocol}//${host}:8000`;
})();

const form = document.getElementById("food-form");
const input = document.getElementById("food-input");
const submitBtn = document.getElementById("submit-btn");

const resultBox = document.getElementById("result");
const resultFood = document.getElementById("result-food");
const resultTier = document.getElementById("result-tier");
const resultExplanation = document.getElementById("result-explanation");
const resultSource = document.getElementById("result-source");

const statusBox = document.getElementById("status");

function showStatus(message) {
  statusBox.textContent = message;
  statusBox.classList.remove("hidden");
}

function clearStatus() {
  statusBox.textContent = "";
  statusBox.classList.add("hidden");
}

function hideResult() {
  resultBox.classList.add("hidden");
}

function renderResult({ food, tier, explanation, source }) {
  resultFood.textContent = food;

  // Reset then apply the tier-specific badge color (badge-A / badge-B / badge-C).
  resultTier.className = "badge";
  const safeTier = String(tier || "").toUpperCase();
  if (safeTier === "A" || safeTier === "B" || safeTier === "C") {
    resultTier.classList.add(`badge-${safeTier}`);
  }
  resultTier.textContent = safeTier || "?";

  resultExplanation.textContent = explanation || "";
  resultSource.textContent = source || "";

  resultBox.classList.remove("hidden");
}

async function classifyFood(food) {
  const response = await fetch(`${API_BASE}/api/food-tier`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ food }),
  });

  // FastAPI returns {"detail": "..."} on 4xx/5xx — surface that message
  // when present, otherwise fall back to a generic HTTP error.
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const errBody = await response.json();
      if (errBody && errBody.detail) detail = errBody.detail;
    } catch (_) {
      /* response had no JSON body — keep the generic message */
    }
    throw new Error(detail);
  }

  return response.json();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const food = input.value.trim();
  if (!food) {
    showStatus("Please enter a food name.");
    return;
  }
  
  clearStatus();
  hideResult();
  submitBtn.disabled = true;
  const originalLabel = submitBtn.textContent;
  submitBtn.textContent = "Classifying…";

  try {
    const data = await classifyFood(food);
    renderResult(data);
  } catch (err) { 
    // Network errors (backend down, CORS, DNS) land here as TypeError.
    const message =
      err instanceof TypeError
        ? `Could not reach the API at ${API_BASE}. Is the backend running?`
        : err.message || "Something went wrong.";
    showStatus(message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = originalLabel;
  }
});
