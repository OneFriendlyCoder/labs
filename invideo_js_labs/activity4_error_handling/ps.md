Problem Description
Create a simple user registration form with client-side validation that ensures proper input for name and age fields. The form should implement error handling and display appropriate messages to users.
Requirements
Form Fields

    Name Field

    Must not be empty
    Should accept text input
    Validation error should show if empty

    Age Field

    Must be a numeric value
    Must be 18 or above
    Validation error should show if invalid

Functionality
    Form should prevent default submission
    Validation should occur on form submission
    Error messages should display in the designated error message area
    Successful submission should show an alert message
    All previous error messages should be cleared before new validation

Expected Validation Behaviors
    Empty Name

    When: User submits form with empty name
    Expected: Error message "Name cannot be empty."

    Invalid Age (Below 18)

    When: User submits form with age < 18
    Expected: Error message "Age must be a number and at least 18."

    Invalid Age (Non-numeric)

    When: User submits form with non-numeric age
    Expected: Error message containing "Age must be a number"

    Successful Submission

    When: User submits form with valid name and age 18
    Expected: Alert message "Form submitted successfully!"
