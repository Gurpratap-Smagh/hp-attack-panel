const logPane = document.getElementById("logPane");
const randomButton = document.getElementById("randomButton");

const appendLog = (message) => {
  logPane.textContent += `${message}\n`;
  logPane.scrollTop = logPane.scrollHeight;
};

const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const ws = new WebSocket(`${protocol}://${window.location.host}/ws`);

ws.onopen = () => {
  appendLog("[ws] connected");
  setInterval(() => ws.readyState === WebSocket.OPEN && ws.send("ping"), 15000);
};

ws.onmessage = (event) => {
  try {
    const data = JSON.parse(event.data);
    appendLog(JSON.stringify(data, null, 2));
  } catch {
    appendLog(event.data);
  }
};

ws.onclose = () => appendLog("[ws] disconnected");

randomButton.addEventListener("click", async () => {
  try {
    const res = await fetch("/fire-random", { method: "POST" });
    const data = await res.json();
    appendLog(`[http] fired payload ${data.payload_id} (${data.status_code})`);
  } catch (err) {
    appendLog(`[error] ${err}`);
  }
});
