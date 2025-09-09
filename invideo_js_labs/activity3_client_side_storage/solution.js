document.addEventListener("DOMContentLoaded", () => {
  const greetingElement = document.getElementById("greeting");
  const nameForm = document.getElementById("nameForm");
  const firstnameInput = document.getElementById("firstname");
  const lastnameInput = document.getElementById("lastname");

  // Load stored names
  const storedFirstName = localStorage.getItem("firstname");
  const storedLastName = localStorage.getItem("lastname");

  if (storedFirstName && storedLastName) {
    greetingElement.textContent = `Hello ${storedFirstName} ${storedLastName}`;
  }

  nameForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const firstname = firstnameInput.value.trim();
    const lastname = lastnameInput.value.trim();

    // Store names in local storage
    localStorage.setItem("firstname", firstname);
    localStorage.setItem("lastname", lastname);

    firstnameInput.value = "";
    lastnameInput.value = "";

    location.reload();
  });
});
