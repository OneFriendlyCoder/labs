# Mini To-Do List Application

## Problem Statement

You are required to implement a simple JavaScript To-Do List application. The application allows users to add tasks, mark tasks as completed, and persist them using the browser's `localStorage`. Your implementation will complete the partially written `script.js` file by filling in the provided `TODO` sections.  

The HTML structure has already been created and contains elements for entering a task, adding it, and displaying the list. **Do not modify the HTML elements or their IDs**. You will work only in `script.js` to implement the functionality.

Your tasks are divided into three main parts:

---

## Part A – Adding Tasks

Implement the `addTask()` function:

1. Read the task text from the input element (`taskInput`) and trim whitespace.
2. Validate that the input is not empty. (This check is already partially handled in the "do not edit zone".)
3. Create a new task object with the following properties:
   - `id`: unique numeric identifier (e.g., `Date.now()`)
   - `text`: the task text
   - `done`: boolean indicating whether the task is completed (`false` by default)
4. Add the new task to the global `tasks` array.
5. Save the updated tasks array to `localStorage` using the provided `saveTasks()` function.
6. Re-render the task list using the provided `renderTasks()` function.
7. Clear the input field and focus it for the next task. (This is handled in the "do not edit zone".)

---

## Part B – Toggle Task Completion

Implement the `toggleDone(id)` function:

1. Locate the task in the `tasks` array using its `id`.
2. Toggle the `done` property of the task (`true` ↔ `false`).
3. Save the updated tasks array to `localStorage`.
4. Re-render the task list so that the DOM reflects the task’s completed state.

---

## Part C – Loading Tasks from Local Storage

Implement the `loadTasks()` function:

1. Read the saved tasks JSON from `localStorage` using the `STORAGE_KEY`.
2. Parse the JSON and validate that it is an array.
3. Assign the parsed tasks to the global `tasks` array.
4. Ensure the application can handle errors if the JSON is invalid.

---

## Initial Setup & Event Wiring

Complete the `window.addEventListener('load', ...)` section:

1. Call `loadTasks()` to load any previously saved tasks.
2. Call `renderTasks()` to display the loaded tasks in the DOM.
3. Wire up the event listeners for adding tasks:
   - Click on the `addBtn` button should call `addTask()`.
   - Pressing `Enter` inside `taskInput` should call `addTask()`.

> **Note:** You may add new JavaScript code as needed, but do not remove or rename the existing HTML elements, their IDs, or the non-editable sections in the provided code.
