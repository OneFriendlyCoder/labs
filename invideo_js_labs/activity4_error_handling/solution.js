document
  .getElementById("userForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Clear previous error messages

    try {
      // Validate name
      if (name === "") {
        throw new Error("Name cannot be empty.");
      }

      // Validate age
      if (isNaN(age) || age < 18) {
        throw new Error("Age must be a number and at least 18.");
      }

      alert("Form submitted successfully!");
    } catch (error) {
      errorMessage.textContent = `Error: ${error.message}`;
    }
  });
