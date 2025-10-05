document.addEventListener("DOMContentLoaded", displayNotes);

function getNotes() {
  // TODO: Retrieve notes from localStorage
}

function addNote() {
  const title = document.getElementById("title").value;
  const body = document.getElementById("body").value;

  if (title && body) {
    const notes = getNotes();
    // TODO: Add a new note to the notes array
    displayNotes();
    document.getElementById("title").value = "";
    document.getElementById("body").value = "";
  } else {
    alert("Please enter both title and body for the note.");
  }
}

function displayNotes() {
  const notesList = document.getElementById("notesList");
  notesList.innerHTML = "";
  const notes = getNotes();

  notes.forEach((note, index) => {
    const noteDiv = document.createElement("div");
    noteDiv.className = "note";
    noteDiv.innerHTML = `<h3>${note.title}</h3><p>${note.body}</p><button onclick="deleteNote(${index})">Delete</button>`;
    notesList.appendChild(noteDiv);
  });
}

function deleteNote(index) {
  const notes = getNotes();
  // TODO: Delete the note at the given index
  displayNotes();
}
