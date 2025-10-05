// ********** JavaScript Lab: Understanding Variables **********
// INSTRUCTIONS:
// 1. Complete the tasks below by filling in the required variable declarations and assignments.
// 2. Use the proper variable declarations: const, let, and var.

// Task 1: Declare and Initialize Variables
// - Use `var` for a variable that can be redeclared (though generally discouraged in modern JavaScript) - to set city to Mumbai
// - Use `let` for variables that may change - to set temperature to 30
// - Use `const` for values that should remain constant - to set country to India

var city = "Mumbai";
let temperature = 30;
const country = "India";

// Log the values to the console
document.getElementById('output').innerHTML += `City: ${city}<br>`;
document.getElementById('output').innerHTML += `Temperature: ${temperature}<br>`;
document.getElementById('output').innerHTML += `Country: ${country}<br>`;

// Task 2: Reassign and Redeclare Variables
// 2.1: Reassign the temperature variable (use `let`) to 35 and log it to the console.

temperature = 35;

document.getElementById('output').innerHTML += `Updated Temperature: ${temperature}<br>`;

// 2.2: Attempt to reassign the country variable (this should cause an error, since it's a const).
// Uncomment the next line to test reassigning a const variable.
// country = "USA"; // This should cause an error

// Task 3: Perform Basic Math Operations Using let Variables, set num1 to 8 and num2 to 4

let num1 = 8;
let num2 = 4;

// Perform additi> wsl --install -d Ubuntu-24.04on and subtraction, and log the results
document.getElementById('output').innerHTML += `Addition: ${num1 + num2}<br>`;
document.getElementById('output').innerHTML += `Subtraction: ${num1 - num2}<br>`;
// Task 4: String Concatenation Using const and let and set firstName to "John" and lastName to "Doe"
let firstName = "John";
let lastName = "Doe";
// Concatenate firstName and lastName to form fullName and log it.

let fullName = firstName + " " + lastName;
document.getElementById('output').innerHTML += `Full Name: ${fullName}<br>`;

// Task 5: Declare and Reassign let Variable
// Use let for variables that may change. Declare a let variable favoriteColor and set it to blue.
let favoriteColor = "blue";
document.getElementById('output').innerHTML += `Original Favorite Color: ${favoriteColor}<br>`;

// Reassign the favoriteColor variable to green
favoriteColor = "green";
document.getElementById('output').innerHTML += `Updated Favorite Color: ${favoriteColor}<br>`;

// Task 6: Preventing Reassignment with const
// Uncomment the line below to see that reassigning a const variable causes an error.

// PI = 3.14; // Uncomment this line to trigger an error during validation

// Task 7: Camel case
let string = "First name of the user";

// Convert the string to camel case
string = "firstNameOfTheUser";

document.getElementById('output').innerHTML += `Camel Case: ${string}<br>`;