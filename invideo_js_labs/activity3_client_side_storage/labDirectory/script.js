document.addEventListener("DOMContentLoaded", () => {
  const greetingElement = document.getElementById("greeting");
  const nameForm = document.getElementById("nameForm");
  const firstnameInput = document.getElementById("firstname");
  const lastnameInput = document.getElementById("lastname");

  const storedFirstName = localStorage; // TODO: get firstname
  const storedLastName = localStorage; // TODO: get lastname

  if (storedFirstName && storedLastName) {
    greetingElement.textContent = `Hello ${storedFirstName} ${storedLastName}`;
  }

  nameForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const firstname = firstnameInput.value.trim();
    const lastname = lastnameInput.value.trim();

    localStorage; // TODO: set firstname
    localStorage; // TODO: set lastname

    firstnameInput.value = "";
    lastnameInput.value = "";

    location.reload();
  });
});
