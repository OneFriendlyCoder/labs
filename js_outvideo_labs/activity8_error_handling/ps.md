Error Handling
Problem Description

In this exercise, you will implement custom error classes and error handling for a simulated API service. The service includes user authentication and time retrieval functionality. Your task is to properly implement the error classes and handle various error scenarios in the API methods.
Requirements
1. Error Classes Implementation

You need to implement the following error classes:

    NetworkError
    Status code: 503
    Used when network connectivity issues occur
    AuthenticationError
    Status code: 401
    Used when authentication credentials are invalid
    MissingUserDataError
    Status code: 404
    Used when required user data (token) is missing
    InvalidEndpointError
    Status code: 400
    Used when an invalid API endpoint is requested

Each error class should:

    Extend the base Error class
    Include appropriate status code
    Set the correct error name
    Accept and store an error message

2. API Service Methods Implementation
authenticateUser(username, password)

    Authenticates user with provided credentials
    Returns a token on successful authentication
    Must handle:
    NetworkError: When network issues occur
    AuthenticationError: When credentials are incorrect
    Unknown errors: Any other unexpected errors
    Only valid credentials are: username="admin", password="password"

getUserLocalTime(token)

    Retrieves user's local time using provided token
    Returns formatted time string
    Must handle:
    NetworkError: When network issues occur
    MissingUserDataError: When token is empty/null
    Unknown errors: Any other unexpected errors

3. Error Handling Requirements

    All error messages must be non-empty strings
    Appropriate error types must be thrown for each scenario
    Network errors occur randomly (50% chance) in the simulation
    Error messages should be user-friendly and descriptive