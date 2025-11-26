// autograder.js
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
function randToken() { return "TG_" + Math.random().toString(36).slice(2, 10); }

async function run() {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
  });
  const page = await browser.newPage();

  const results = { data: [] };

  function push(testid, status, score, message = "", maxMarks = 1) {
    results.data.push({
      testid,
      status,
      score,
      "maximum marks": maxMarks,
      message
    });
  }

  const indexPath = path.join("/home/labDirectory/", "index.html");
  if (!fs.existsSync(indexPath)) {
    push("FileCheck", "failure", 0, "index.html not found: " + indexPath);
    fs.writeFileSync(path.join(__dirname, "..", "evaluate.json"), JSON.stringify(results, null, 2));
    await browser.close();
    return;
  }

  await page.goto("file://" + indexPath, { waitUntil: "load" });
  await wait(200);

  async function renderedTasks() {
    return page.evaluate(() => {
      try {
        const nodes = Array.from(document.querySelectorAll(".task-item"));
        const fallback = document.getElementById("taskList");
        const items = nodes.length ? nodes : (fallback ? Array.from(fallback.children) : []);
        return items.map(n => {
          const checkbox = n.querySelector("input[type='checkbox']");
          const textEl = n.querySelector(".task-text") || n.querySelector("span") || n;
          return {
            domHtml: n.outerHTML,
            text: textEl ? (textEl.textContent || "").trim() : "",
            hasDoneClass: !!(textEl ? textEl.classList.contains("done") : n.classList.contains("done")),
            checkboxExists: !!checkbox,
            checkboxChecked: !!(checkbox && checkbox.checked),
            datasetId: n.dataset && n.dataset.id ? String(n.dataset.id) : null
          };
        });
      } catch (e) { return []; }
    });
  }

  async function localStorageTasks() {
    return page.evaluate(() => {
      try {
        const raw = localStorage.getItem(window.STORAGE_KEY || "mini_todo_tasks_v1");
        if (!raw) return [];
        const parsed = JSON.parse(raw);
        if (!Array.isArray(parsed)) return [];
        return parsed.map(t => ({ id: String(t.id), text: String(t.text), done: Boolean(t.done) }));
      } catch (e) { return []; }
    });
  }

  async function setInput(val) {
    const el = await page.$("#taskInput");
    if (!el) throw new Error("taskInput not found");
    await page.$eval("#taskInput", (e, v) => e.value = v, val);
  }

  async function clickAdd() {
    const btn = await page.$("#addBtn");
    if (btn) { await btn.click(); return; }
    await page.evaluate(() => { if (typeof addTask === "function") addTask(); });
  }

  async function resetStatePreserveFuncs() {
    await page.evaluate(() => {
      try {
        localStorage.removeItem(window.STORAGE_KEY || "mini_todo_tasks_v1");
        const tl = document.getElementById("taskList"); if (tl) tl.innerHTML = "";
        const inp = document.getElementById("taskInput"); if (inp) { inp.value = ""; inp.blur(); }
      } catch (e) {}
    });
    await wait(80);
  }

  // ------------------- Part A: addTask -------------------
  try {
    await resetStatePreserveFuncs();
    const token = randToken();
    await setInput(token);
    await clickAdd();
    await wait(250);

    const rendered = await renderedTasks();
    const stored = await localStorageTasks();

    const foundDom = rendered.find(r => r.text.toLowerCase().includes(token.toLowerCase()));
    const foundStorage = stored.find(s => s.text.toLowerCase().includes(token.toLowerCase()));
    const idOk = !!(foundStorage && foundStorage.id && !Number.isNaN(Number(foundStorage.id)));

    if (foundDom && foundStorage && idOk) {
      push("PartA-addTask", "success", 4, "Task added successfully, saved in localStorage and rendered in DOM", 4);
    } else {
      const reasons = [];
      if (!foundStorage) reasons.push("Task not saved to localStorage");
      if (!idOk) reasons.push("Task id missing or invalid in storage");
      if (!foundDom) reasons.push("Task not rendered in DOM");
      push("PartA-addTask", "failure", 0, reasons.join("; "), 4);
    }
  } catch (e) {
    push("PartA-addTask", "failure", 0, "Exception: " + String(e), 4);
  }

  // ------------------- Part B: toggleDone -------------------
  try {
    await resetStatePreserveFuncs();
    const token = randToken();
    await setInput(token);
    await clickAdd();
    await wait(220);

    const initialStored = await localStorageTasks();
    const addedTask = initialStored.find(t => t.text.toLowerCase().includes(token.toLowerCase()));

    if (!addedTask) {
      push("PartB-toggleDone", "failure", 0, "Task not found in localStorage; cannot test toggleDone", 3);
    } else {
      const taskId = addedTask.id;
      let stepResults = [];

      await page.evaluate((id) => {
        if (typeof toggleDone === "function") toggleDone(Number(id));
      }, taskId);
      await wait(200);

      const storedAfter = await localStorageTasks();
      const taskAfter = storedAfter.find(t => t.id === taskId);
      if (!taskAfter) stepResults.push("Task disappeared from localStorage after toggle");
      else if (taskAfter.done === addedTask.done) stepResults.push("Task 'done' value not toggled in localStorage");
      else stepResults.push("Task 'done' value toggled in localStorage ✔");

      const renderedAfter = await renderedTasks();
      const domTask = renderedAfter.find(t => t.text.toLowerCase().includes(token.toLowerCase()));
      if (!domTask) stepResults.push("Task missing in DOM after toggle");
      else if (domTask.hasDoneClass !== taskAfter.done) stepResults.push("DOM does not reflect task 'done' state correctly");
      else stepResults.push("DOM updated with task 'done' state ✔");

      if (stepResults.every(r => r.includes("✔"))) {
        push("PartB-toggleDone", "success", 3, stepResults.join("; "), 3);
      } else {
        push("PartB-toggleDone", "failure", 0, stepResults.join("; "), 3);
      }
    }
  } catch (e) {
    push("PartB-toggleDone", "failure", 0, "Exception: " + String(e), 3);
  }

  // ------------------- Part C: loadTasks -------------------
  try {
    const sample = [
      { id: 1010101, text: "Saved A AG", done: false },
      { id: 2020202, text: "Saved B AG", done: true }
    ];
    await page.evaluate((s) => {
      localStorage.setItem(window.STORAGE_KEY || "mini_todo_tasks_v1", JSON.stringify(s));
      const tl = document.getElementById("taskList"); if (tl) tl.innerHTML = "";
      const inp = document.getElementById("taskInput"); if (inp) inp.value = "";
    }, sample);

    await page.reload({ waitUntil: "load" });
    await wait(300);

    const rendered = await renderedTasks();
    const stored = await localStorageTasks();

    const hasA = stored.some(s => s.text.toLowerCase().includes("saved a ag"));
    const hasBDone = stored.some(s => s.text.toLowerCase().includes("saved b ag") && s.done === true);
    const domCount = rendered.length;
    const domBDone = rendered.some(r => r.text.toLowerCase().includes("saved b ag") && r.hasDoneClass);

    if (hasA && hasBDone && domCount >= 2 && domBDone) {
      push("PartC-loadTasks", "success", 3, "Tasks loaded from localStorage correctly; DOM rendered with expected items and done flags", 3);
    } else {
      const reasons = [];
      if (!hasA) reasons.push("Saved A missing from storage after reload");
      if (!hasBDone) reasons.push("Saved B done flag not set in storage after reload");
      if (domCount < 2) reasons.push("Not enough DOM items after reload");
      if (!domBDone) reasons.push("Rendered Saved B missing .done class");
      push("PartC-loadTasks", "failure", 0, reasons.join("; "), 3);
    }
  } catch (e) {
    push("PartC-loadTasks", "failure", 0, "Exception: " + String(e), 3);
  }

  // ------------------- Write evaluate.json -------------------
  try {
    const outPath = path.join(__dirname, "..", "evaluate.json");
    fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
  } catch (e) {
    console.error("Could not write evaluate.json:", e);
  }

  await browser.close();
}

run().catch(e => console.error(e));
