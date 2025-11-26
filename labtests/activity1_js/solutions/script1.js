let tasks = [];
const STORAGE_KEY = 'mini_todo_tasks_v1';
const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');

function addTask() {
  const text = taskInput.value.trim();
  if (!text) {
    alert('Please enter a task before adding.');
    return;
  }
  const task = {
    id: Date.now(),
    text: text,
    done: false
  };
  tasks.push(task);
  saveTasks();
  renderTasks();
  taskInput.value = '';
  taskInput.focus();
}

function renderTasks() {
  taskList.innerHTML = '';
  tasks.forEach(task => {
    const item = document.createElement('div');
    item.className = 'task-item';
    item.dataset.id = String(task.id);

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.setAttribute('aria-label', 'Toggle task done');
    checkbox.checked = !!task.done;
    checkbox.addEventListener('change', () => {
      toggleDone(task.id);
    });

    const textEl = document.createElement('span');
    textEl.className = 'task-text';
    textEl.textContent = task.text;

    if (task.done) textEl.classList.add('done');

    item.appendChild(checkbox);
    item.appendChild(textEl);
    taskList.appendChild(item);
  });
}

function toggleDone(id) {
  const idx = tasks.findIndex(t => t.id === id);
  if (idx === -1) return;
  tasks[idx].done = !tasks[idx].done;
  saveTasks();
  renderTasks();
}

function saveTasks() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  } catch (e) {
    console.error('Could not save tasks to localStorage', e);
  }
}

function loadTasks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      tasks = parsed.map(t => ({
        id: Number(t.id),
        text: String(t.text),
        done: Boolean(t.done)
      }));
    }
  } catch (e) {
    console.error('Could not load tasks from localStorage', e);
  }
}

window.addEventListener('load', () => {
  loadTasks();
  renderTasks();
  addBtn.addEventListener('click', addTask);
  taskInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addTask();
  });
});
