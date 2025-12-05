let tasks = []; // global tasks array

const STORAGE_KEY = 'mini_todo_tasks_v1';
const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');

/* -------------------------
   Part A - Adding Tasks
   ------------------------- */
function addTask() {

  // TODO: Read text from taskInput and trim it
  // const text = ...
  const text = taskInput.value.trim();

  //-------Do not edit zone-------
  if(!text){
    console.log('Please enter a task before adding.');
    return;
  }
  //-------Do not edit zone-------

  // TODO: Create a task object { id: Date.now(), text: text, done: false }
    const task = {
    id: Date.now(),
    text: text,
    done: false
  };
  // TODO: Push the task into the global tasks array
  tasks.push(task);
  // TODO: Save tasks to localStorage using saveTasks()
  saveTasks();
  // TODO: Call renderTasks()
  renderTasks();

  //-------Do not edit zone-------
  taskInput.value = '';
  taskInput.focus();
  //-------Do not edit zone-------

}

// Renders the Tasks
//-------Do not edit zone-------
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
//-------Do not edit zone-------


/* -------------------------
   Part B - toggleDone()
   ------------------------- */
function toggleDone(id) {

  // TODO: Find the task by id
  const idx = tasks.findIndex(t => t.id === id);
  if (idx === -1) return;
  // TODO: Toggle the task.done value
  tasks[idx].done = !tasks[idx].done;
  // TODO: Save tasks to localStorage
  saveTasks();
  // TODO: Re-render the task list
  renderTasks();
}

// functions that saves the task in localStorage
//-------Do not edit zone-------
function saveTasks() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  } catch (e) {
    console.error('Could not save tasks to localStorage', e);
  }
}
//-------Do not edit zone-------


/* -------------------------
   Part C - Loading Tasks
   ------------------------- */
function loadTasks() {
  try{

  // TODO: Read saved JSON from localStorage
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return;
  // TODO: Parse it and validate it is an array
  const parsed = JSON.parse(raw);
  // TODO: Assign parsed tasks to the global tasks array
    if (Array.isArray(parsed)) {
      tasks = parsed.map(t => ({
        id: Number(t.id),
        text: String(t.text),
        done: Boolean(t.done)
      }));
    }
  }catch(e){
    console.error('Could not load tasks from localStorage',e)
  }
}

/* -------------------------
   Wiring events & initial load
   ------------------------- */
window.addEventListener('load', () => {

  // TODO: Call loadTasks()
  loadTasks();
  // TODO: Call renderTasks()
  renderTasks();
  
//-------Do not edit zone-------
  addBtn.addEventListener('click', addTask);
  taskInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addTask();
  });
//-------Do not edit zone-------
});
