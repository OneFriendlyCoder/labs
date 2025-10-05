Notes Application
Objective

Create a simple notes application using JavaScript that allows users to add, display, and delete notes. This application should store notes persistently in localStorage, so that users can access their notes even after refreshing the page.
Requirements

    Add a Note: Users should be able to add a new note by entering a title and body. If either the title or body is missing, an alert should inform the user to complete both fields.
    Display Notes: When the page loads, the application should display all saved notes. Each note should show its title and body, along with a "Delete" button to remove it.
    Delete a Note: Users should be able to delete a note by clicking the "Delete" button associated with each note. This should remove the note both from the display and from localStorage.

Code Skeleton

    getNotes(): Retrieve and parse notes from localStorage.
    addNote(): Add a new note to the notes array and update localStorage.
    displayNotes(): Loop through all notes and render each with a delete option.
    deleteNote(index): Remove the note at the specified index from localStorage.