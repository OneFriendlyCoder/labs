Problem Statement :
Develop a web-based greeting application that stores a user's first and last name in localStorage to personalize their experience across visits. The application should display a greeting with the users name if their details are stored in the browser's localStorage.
When a user visits the application for the first time, they should be prompted to enter their first and last name in a form. Upon submission, these details should be saved to localStorage and displayed as a greeting message on the page. If the user revisits the page, the stored details should be retrieved from localStorage and used to automatically display a personalized greeting.

Key Functionality to Implement : 
    Storage and Retrieval: Modify the code to retrieve the first name and last name from localStorage upon page load and display a greeting if both values exist.
    Data Persistence: Update localStorage with the user's first and last name upon form submission so that their information persists between sessions.