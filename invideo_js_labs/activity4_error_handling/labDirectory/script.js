document
  .getElementById("userForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value.trim();
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = ""; // Clear previous error messages

    try {
      // Name shoudn't be empty
      if (isNaN(name)) {
        // Throw error
      }

      // Validate age, should be >= 18
      if (isNaN(age)) {
        // Throw error
      }

      alert("Form submitted successfully!");
    } catch (error) {
      errorMessage.textContent = `Error: ${error.message}`;
    }
  });
