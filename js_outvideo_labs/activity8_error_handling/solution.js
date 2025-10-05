class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = "NetworkError";
    this.status = 503;
  }
}

class AuthenticationError extends Error {
  constructor(message) {
    super(message);
    this.name = "AuthenticationError";
    this.status = 401;
  }
}

class MissingUserDataError extends Error {
  constructor(message) {
    super(message);
    this.name = "MissingUserDataError";
    this.status = 404;
  }
}

class InvalidEndpointError extends Error {
  constructor(message) {
    super(message);
    this.name = "InvalidEndpointError";
    this.status = 400;
  }
}

class APIService {
  constructor() {}

  async simulateRequest(endpoint, username, password, token) {
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
    try {
      return await this.simulateRequest(endpoint, username, password, token);
    } catch (error) {
      throw error;
    }
  }

  async authenticateUser(username, password) {
    try {
      const response = await this.fetchData("/auth", username, password, null);
      return response.token;
    } catch (error) {
      if (error instanceof NetworkError) {
        throw new Error("A network error occurred. Please try again.");
      } else if (error instanceof AuthenticationError) {
        throw new Error(
          "Authentication failed. Please check your credentials and try again.",
        );
      }
      throw new Error("An unknown error has occured.");
    }
  }

  async getUserLocalTime(token) {
    try {
      const response = await this.fetchData("/time", null, null, token);
      return `User's local time is: ${response.data}`;
    } catch (error) {
      if (error instanceof NetworkError) {
        throw new Error("A network error occurred. Please try again.");
      } else if (error instanceof MissingUserDataError) {
        throw new Error("User data not found. Please login again.");
      }
      throw new Error("An unknown error has occured.");
    }
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
