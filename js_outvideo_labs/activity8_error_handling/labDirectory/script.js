// TODO: Implement NetworkError with status code 503
class NetworkError {}

// TODO: Implement AuthenticationError with status code 401
class AuthenticationError {}

// TODO: Implement MissingUserDataError with status code 404
class MissingUserDataError {}

// TODO: Implement InvalidEndpointError with status code 400
class InvalidEndpointError {}

class APIService {
  constructor() {}

  async simulateRequest(endpoint, username, password, token) {
    // Do not modify this method
    if (Math.random() < 0.5) {
      throw new NetworkError();
    }

    if (endpoint === "/auth") {
      if (username !== "admin" || password !== "password") {
        throw new AuthenticationError();
      }
      return {
        data: "Authentication successful",
        token: "simulated-token-12345",
      };
    }

    if (endpoint === "/time") {
      if (!token) {
        throw new MissingUserDataError();
      }
      const userLocalTime = new Date().toLocaleString(); // Simulated time
      return { data: userLocalTime };
    }

    throw new InvalidEndpointError(`Invalid endpoint: ${endpoint}`);
  }

  async fetchData(endpoint, username, password, token) {
    // Do not modify this method
    try {
      return await this.simulateRequest(endpoint, username, password, token);
    } catch (error) {
      throw error;
    }
  }

  async authenticateUser(username, password) {
    // TODO: Handle NetworkError, AuthenticationError and unknown errors by throwing appropriate error message
    const response = await this.fetchData("/auth", username, password, null);
    return response.token;
  }

  async getUserLocalTime(token) {
    // TODO: Handle NetworkError, MissingUserDataError and unknown errors by throwing appropriate error message
    const response = await this.fetchData("/time", null, null, token);
    return `User's local time is: ${response.data}`;
  }
}

const apiService = new APIService();

document.getElementById("login-btn").addEventListener("click", async () => {
  document.getElementById("error-message").classList.add("hidden");

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  document.getElementById("loading").classList.remove("hidden");

  try {
    const token = await apiService.authenticateUser(username, password);
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("user-data").classList.remove("hidden");
    document.getElementById("fetch-btn").dataset.token = token; // Store token in the button's data attribute
  } catch (error) {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("error-message").classList.remove("hidden");
    document.getElementById("error-text").textContent = error.message;
    document.getElementById("fetch-btn").dataset.token = "";
    document.getElementById("user-data").classList.add("hidden");
  }
});

document.getElementById("fetch-btn").addEventListener("click", async () => {
  document.getElementById("error-message").classList.add("hidden");
  document.getElementById("user-info").textContent = "";

  const token = document.getElementById("fetch-btn").dataset.token; // Get token from the button's data attribute

  document.getElementById("loading").classList.remove("hidden");
  try {
    const userLocalTime = await apiService.getUserLocalTime(token);
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("user-info").textContent = userLocalTime;
  } catch (error) {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("error-message").classList.remove("hidden");
    document.getElementById("error-text").textContent = error.message;
  }
});
