const $ = (id) => document.getElementById(id);

async function api(method, url, body) {
  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = res.status === 204 ? null : await res.json();
  return { ok: res.ok, data };
}

function showTimer(t) {
  const m = String(Math.floor(t.remaining / 60)).padStart(2, "0");
  const s = String(t.remaining % 60).padStart(2, "0");
  $("clock").textContent = `${m}:${s}`;
  $("mode").textContent = t.mode.replace("_", " ");
  $("completed").textContent = t.completed;
}

async function loadTasks() {
  const { data } = await api("GET", "/api/tasks");
  $("tasks").innerHTML = "";
  for (const task of data) {
    const li = document.createElement("li");
    const span = document.createElement("span");
    span.textContent = task.title;
    if (task.done) span.style.textDecoration = "line-through";
    const done = document.createElement("button");
    done.textContent = "Done";
    done.onclick = async () => { await api("POST", `/api/tasks/${task.id}/complete`); loadTasks(); };
    const del = document.createElement("button");
    del.textContent = "Delete";
    del.onclick = async () => { await api("DELETE", `/api/tasks/${task.id}`); loadTasks(); };
    li.append(span, done, del);
    $("tasks").append(li);
  }
}

$("start").onclick = async () => showTimer((await api("POST", "/api/timer/start")).data);
$("pause").onclick = async () => showTimer((await api("POST", "/api/timer/pause")).data);
$("reset").onclick = async () => showTimer((await api("POST", "/api/timer/reset")).data);

$("save").onclick = async () => {
  const res = await api("POST", "/api/settings", {
    work: Number($("work").value),
    break: Number($("break").value),
  });
  $("settings-error").textContent = res.ok ? "" : res.data.error;
  if (res.ok) showTimer(res.data);
};

$("add-task").onclick = async () => {
  const res = await api("POST", "/api/tasks", { title: $("task-title").value });
  $("task-error").textContent = res.ok ? "" : res.data.error;
  if (res.ok) { $("task-title").value = ""; loadTasks(); }
};

setInterval(async () => showTimer((await api("POST", "/api/timer/tick", { seconds: 1 })).data), 1000);

api("GET", "/api/timer").then((r) => showTimer(r.data));
loadTasks();
