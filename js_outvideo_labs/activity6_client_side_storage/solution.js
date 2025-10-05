document.addEventListener("DOMContentLoaded", displayNotes);

function getNotes() {
  return JSON.parse(localStorage.getItem("notes")) || [];
}

function addNote() {
  const title = document.getElementById("title").value;
  const body = document.getElementById("body").value;

  if (title && body) {
    const notes = getNotes();
    notes.push({ title, body });
    localStorage.setItem("notes", JSON.stringify(notes));
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
  notes.splice(index, 1);
  localStorage.setItem("notes", JSON.stringify(notes));
  displayNotes();
}
