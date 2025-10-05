Problem Statement: JavaScript Event Handling - To-Do List Activity


In this activity, you'll work with JavaScript to complete three functions for a To-Do list application: `filterItems`, `deleteItem`, and `clearList`. These functions will enable users to filter, delete, and clear tasks in the list. The basic HTML structure and some CSS styling are provided, and you'll implement the JavaScript code to manage user interactions effectively.


---


Overview


The To-Do list application includes the following features:

1. Adding Items - When the "Add Item" button is clicked, the app prompts the user to enter a new item. This item is then added to the list.

2. Filter Items - As you type in the filter input box, the list dynamically displays only those items that match the entered text, making it easy to find specific tasks.

3. Delete Individual Item - Each item in the list has a "Delete" button, which allows users to remove the specific task with one click.

4. Clear List - The "Clear List" button removes all tasks at once, allowing users to reset their list when desired.

1. Updating Items - When an item is clicked other than the delete button's area, the app prompts the user to edit the list entry.

---


Task Requirements


1. Filter Items

- Implement the `filterItems` function to display only the list items that match the text in the filter input box.(Need not be just prefix match)

- The function should:

- Respond to the `input` event on the filter text box.

- Hide list items that don't match the entered filter text (case-insensitive).


2. Delete Individual Item

- Implement the `deleteItem` function, which deletes the specific item in the list when the "Delete" button next to it is clicked.

- Each list item has a `deleteBtn` button that should call this function to remove the corresponding item from the DOM.


3. Clear List

- Implement the `clearList` function to delete all tasks from the list when the "Clear List" button is clicked.


---


How the Application Works


- Adding Items: The "Add Item" button opens a prompt for users to enter the new task's name. The entered item is appended to the list, with a delete button next to it.


- Filter Functionality: The `filterItems` function filters the list in real-time based on the text input, making it easier to locate specific tasks. Only items matching the text in the filter input box are displayed, and the rest are hidden.


- Delete Functionality: Each list item has a delete button, allowing users to remove that item individually. This functionality is handled by the `deleteItem` function.


- Clear List Functionality: The "Clear List" button removes all tasks from the list by calling the `clearList` function, effectively resetting the To-Do list.


---


Instructions


- Write the JavaScript code in `script.js` to complete the functionality for each of these tasks.

- Ensure the functions respond correctly to the respective button clicks and input events.

- Test that filtering, deleting individual items, and clearing all items function as described.


---


Testing Your Solution


Once completed, check that:

- Filter Items - The filter input dynamically shows matching items as you type.

- Delete Individual Item - The delete button on each item correctly removes that item from the list.

- Clear List - The clear button removes all items from the list.