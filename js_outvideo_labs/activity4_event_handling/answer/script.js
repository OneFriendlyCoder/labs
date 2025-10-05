// Function to add a new item to the list
function addItem() {
    const newItem = prompt("Enter a new item:");
    if (newItem) {
        const li = document.createElement("li");
        li.textContent = newItem;
        
        // Add a delete button for the new item
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.className = "deleteBtn";
        li.appendChild(deleteBtn);

        document.getElementById("itemList").appendChild(li);
    }
}

// Function to filter items based on user input
function filterItems(event) {
    const filterText = event.target.value.toLowerCase();
    const items = document.querySelectorAll("#itemList li");

    items.forEach(item => {
        const itemText = item.firstChild.textContent.toLowerCase();
        if (itemText.includes(filterText)) {
            item.style.display = "";
        } else {
            item.style.display = "none";
        }
    });
}

// Function to update the item when clicked
function updateItem(event) {
    if (event.target.tagName === "LI") {
        const updatedText = prompt("Update item text:", event.target.firstChild.textContent);
        if (updatedText) {
            event.target.firstChild.textContent = updatedText;
        }
    }
}

// Function to delete an item when the delete button is clicked
function deleteItem(event) {
    if (event.target.classList.contains("deleteBtn")) {
        const li = event.target.parentElement;
        li.remove();
    }
}

// Function to clear all items in the list
function clearList() {
    document.getElementById("itemList").innerHTML = "";
}

// Event listeners for the buttons and input
document.getElementById('addItem').addEventListener('click', addItem);
document.getElementById('filterInput').addEventListener('keyup', filterItems);
document.getElementById('clearList').addEventListener('click', clearList);

// Event delegation for list items
document.getElementById('itemList').addEventListener('click', function(event) {
    console.log(event.target);
    if (event.target.classList.contains('deleteBtn')) {
        deleteItem(event);
    } else {
        updateItem(event);
    }
});
