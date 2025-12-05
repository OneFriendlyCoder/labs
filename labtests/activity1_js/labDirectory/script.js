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


  //-------Do not edit zone-------
  if(!text){
    console.log('Please enter a task before adding.');
    return;
  }
  //-------Do not edit zone-------

  // TODO: Create a task object { id: Date.now(), text: text, done: false }

  // TODO: Push the task into the global tasks array

  // TODO: Save tasks to localStorage using saveTasks()

  // TODO: Call renderTasks()


  //-------Do not edit zone-------
  taskInput.value = '';
  taskInput.focus();
  //-------Do not edit zone-------

}

// Renders the Tasks
//-------Do not edit zone-------
function resetTasks() {
  localStorage.removeItem(STORAGE_KEY);
  tasks = [];
  renderTasks();
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
//-------Do not edit zone-------


/* -------------------------
   Part B - toggleDone()
   ------------------------- */
function toggleDone(id) {

  // TODO: Find the task by id

  // TODO: Toggle the task.done value

  // TODO: Save tasks to localStorage

  // TODO: Re-render the task list
}


//-------Do not edit zone-------
function saveTasks() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  } catch (e) {
    console.error('Could not save tasks to localStorage', e);
  }
}

function loadTasks() {
  try{
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
  }catch(e){
    console.error('Could not load tasks from localStorage',e)
  }
}

window.addEventListener('load', () => {
  loadTasks();
  renderTasks();  
  addBtn.addEventListener('click', addTask);
  taskInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addTask();
  });
  document.getElementById('resetBtn').addEventListener('click', resetTasks);
//-------Do not edit zone-------
});
