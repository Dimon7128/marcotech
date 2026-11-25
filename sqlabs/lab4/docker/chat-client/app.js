const form = document.querySelector("#message-form");
const input = document.querySelector("#message");
const transcript = document.querySelector("#transcript");
const sendButton = document.querySelector("#send-button");
const sendLabel = document.querySelector("#send-label");
const clearButton = document.querySelector("#clear-chat");
const connection = document.querySelector("#connection");
const connectionLabel = document.querySelector("#connection-label");
const count = document.querySelector("#character-count");
const formError = document.querySelector("#form-error");
const examples = Array.from(document.querySelectorAll("[data-example]"));
let busy = false;

function setConnection(online) {
  connection.classList.toggle("online", online);
  connection.classList.toggle("offline", !online);
  connectionLabel.textContent = online ? "Model connected" : "Model unavailable";
}

// Relative URLs go to Nginx, which forwards /api requests inside the Compose network.
async function apiRequest(path, options = {}) {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 12000);
  try {
    const response = await fetch("/api" + path, {
      ...options,
      signal: controller.signal,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      let detail = "Request failed (HTTP " + response.status + ").";
      if (typeof data.detail === "string") {
        detail = data.detail;
      } else if (Array.isArray(data.detail)) {
        detail = "The model rejected this message: " + data.detail.map((item) => item.msg).join("; ");
      }
      const error = new Error(detail);
      error.status = response.status;
      throw error;
    }
    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("The model took too long to respond. Please try again.");
    }
    if (error instanceof TypeError) {
      throw new Error("Could not reach the service. Check the connection and try again.");
    }
    throw error;
  } finally {
    window.clearTimeout(timeout);
  }
}

async function checkConnection() {
  connection.disabled = true;
  try {
    const data = await apiRequest("/health");
    setConnection(data.status === "ok");
  } catch {
    setConnection(false);
  } finally {
    connection.disabled = false;
  }
}

function scrollConversation() {
  transcript.scrollTop = transcript.scrollHeight;
}

function addMessage(role, text, state = "") {
  const row = document.createElement("article");
  row.className = "message " + role;
  const avatar = document.createElement("span");
  avatar.className = "avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "You" : "s.";
  const content = document.createElement("div");
  content.className = "message-content";
  const name = document.createElement("span");
  name.className = "message-name";
  name.textContent = role === "user" ? "You" : "SMS Classifier";
  const bubble = document.createElement("div");
  bubble.className = "bubble" + (state ? " " + state : "");
  // Message text is rendered as text, never as HTML.
  bubble.textContent = text;
  content.append(name, bubble);
  row.append(avatar, content);
  transcript.append(row);
  scrollConversation();
  return bubble;
}

function showPrediction(bubble, label, duration) {
  bubble.className = "bubble";
  bubble.replaceChildren();
  const title = document.createElement("p");
  title.className = "prediction-title";
  const badge = document.createElement("span");
  badge.className = "label-badge " + label;
  badge.textContent = label.toUpperCase();
  title.append(badge, document.createTextNode("Classified as " + label));
  const description = document.createElement("p");
  description.className = "prediction-description";
  description.textContent = label === "spam"
    ? "The saved model predicts this message is spam."
    : "The saved model predicts this is a regular message.";
  const meta = document.createElement("p");
  meta.className = "prediction-meta";
  meta.textContent = "Saved pipeline · Round trip " + Math.round(duration) + " ms";
  bubble.append(title, description, meta);
  scrollConversation();
}

function updateInput() {
  count.textContent = input.value.length + " / 2000";
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 135) + "px";
}

function setBusy(value) {
  busy = value;
  sendButton.disabled = value;
  clearButton.disabled = value;
  input.disabled = value;
  examples.forEach((button) => { button.disabled = value; });
  sendLabel.textContent = value ? "Sending…" : "Classify";
}

function clearChat() {
  transcript.replaceChildren();
  addMessage("assistant", "Hi! Send me a sample SMS and I’ll classify it as spam or ham. You can also start with one of the examples below.");
  input.value = "";
  formError.textContent = "";
  updateInput();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  const message = input.value.trim();
  if (Array.from(message).length < 2) {
    formError.textContent = "Enter at least two non-space characters.";
    input.focus();
    return;
  }
  formError.textContent = "";
  addMessage("user", message);
  input.value = "";
  updateInput();
  const reply = addMessage("assistant", "Classifying your message…", "pending");
  setBusy(true);
  const started = performance.now();
  try {
    const data = await apiRequest("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (data.label !== "spam" && data.label !== "ham") {
      const error = new Error("The model returned an unexpected response. Check the API contract.");
      error.status = 200;
      throw error;
    }
    showPrediction(reply, data.label, performance.now() - started);
    setConnection(true);
  } catch (error) {
    reply.className = "bubble error";
    reply.textContent = error.message;
    // A validation error means the API was reachable; a proxy/network error does not.
    setConnection(error.status >= 200 && error.status < 500);
    input.value = message;
    updateInput();
    scrollConversation();
  } finally {
    setBusy(false);
    input.focus();
  }
});

input.addEventListener("input", () => {
  formError.textContent = "";
  updateInput();
});
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    form.requestSubmit();
  }
});
examples.forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.example;
    formError.textContent = "";
    updateInput();
    input.focus();
  });
});
clearButton.addEventListener("click", clearChat);
connection.addEventListener("click", checkConnection);

clearChat();
checkConnection();
