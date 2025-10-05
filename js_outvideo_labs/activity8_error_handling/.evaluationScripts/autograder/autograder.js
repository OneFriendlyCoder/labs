const fs = require("fs");
const path = require("path");

const evalContext = {};
const scriptContent = fs.readFileSync(__dirname + "/script.js", "utf8");
const relevantCode = scriptContent.split("document.getElementById")[0];

const setupCode = `
    ${relevantCode}
    return {
        NetworkError,
        AuthenticationError,
        MissingUserDataError,
        InvalidEndpointError,
        APIService
    };
`;

const evalFunction = new Function(setupCode);
const {
  NetworkError,
  AuthenticationError,
  MissingUserDataError,
  InvalidEndpointError,
  APIService,
} = evalFunction();

async function runTest(testFunction, attempts = 10) {
  let successCount = 0;
  let networkErrorCount = 0;
  let lastError = null;

  for (let i = 0; i < attempts; i++) {
    try {
      await testFunction();
      successCount++;
    } catch (error) {
      lastError = error;
      if (error.message && error.message.includes("network error")) {
        networkErrorCount++;
      }
    }
  }

  return {
    successCount,
    networkErrorCount,
    lastError,
  };
}

async function runAllTests() {
  const testResults = { data: [] };

  try {
    const error = new NetworkError("Test error");
    testResults.data.push({
      testid: "NetworkErrorImpl",
      status: error.name === "NetworkError" && error.status === 503 ? "success" : "fail",
      score: error.name === "NetworkError" && error.status === 503 ? 1 : 0,
      "maximum marks": 1,
      message: "NetworkError implementation test",
    });
  } catch {
    testResults.data.push({
      testid: "NetworkErrorImpl",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "NetworkError implementation failed",
    });
  }

  try {
    const error = new AuthenticationError("Test error");
    testResults.data.push({
      testid: "AuthenticationErrorImpl",
      status: error.name === "AuthenticationError" && error.status === 401 ? "success" : "fail",
      score: error.name === "AuthenticationError" && error.status === 401 ? 1 : 0,
      "maximum marks": 1,
      message: "AuthenticationError implementation test",
    });
  } catch {
    testResults.data.push({
      testid: "AuthenticationErrorImpl",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "AuthenticationError implementation failed",
    });
  }

  try {
    const error = new MissingUserDataError("Test error");
    testResults.data.push({
      testid: "MissingUserDataErrorImpl",
      status: error.name === "MissingUserDataError" && error.status === 404 ? "success" : "fail",
      score: error.name === "MissingUserDataError" && error.status === 404 ? 1 : 0,
      "maximum marks": 1,
      message: "MissingUserDataError implementation test",
    });
  } catch {
    testResults.data.push({
      testid: "MissingUserDataErrorImpl",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "MissingUserDataError implementation failed",
    });
  }

  try {
    const error = new InvalidEndpointError("Test error");
    testResults.data.push({
      testid: "InvalidEndpointErrorImpl",
      status: error.name === "InvalidEndpointError" && error.status === 400 ? "success" : "fail",
      score: error.name === "InvalidEndpointError" && error.status === 400 ? 1 : 0,
      "maximum marks": 1,
      message: "InvalidEndpointError implementation test",
    });
  } catch {
    testResults.data.push({
      testid: "InvalidEndpointErrorImpl",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "InvalidEndpointError implementation failed",
    });
  }

  const api = new APIService();

  const authSuccess = await runTest(async () => {
    const token = await api.authenticateUser("admin", "password");
    if (!token || typeof token !== "string" || token.length === 0) {
      throw new Error("Invalid token returned");
    }
  });

  testResults.data.push({
    testid: "AuthenticateUserSuccess",
    status: authSuccess.successCount > 0 ? "success" : "fail",
    score: authSuccess.successCount > 0 ? 1 : 0,
    "maximum marks": 1,
    message: `Authentication with correct credentials (${authSuccess.successCount} successes, ${authSuccess.networkErrorCount} network errors)`,
  });

  const authFailure = await runTest(async () => {
    try {
      await api.authenticateUser("wrong", "credentials");
      throw new Error("Should have thrown AuthenticationError");
    } catch (error) {
      if (!error.message.includes("Authentication failed")) throw error;
    }
  });

  testResults.data.push({
    testid: "AuthenticateUserFailure",
    status: authFailure.successCount > 0 ? "success" : "fail",
    score: authFailure.successCount > 0 ? 1 : 0,
    "maximum marks": 1,
    message: `Authentication with incorrect credentials (${authFailure.successCount} proper error handling)`,
  });

  const timeSuccess = await runTest(async () => {
    const result = await api.getUserLocalTime("valid-token");
    if (!result || !result.includes("User's local time is:")) {
      throw new Error("Invalid time format returned");
    }
  });

  testResults.data.push({
    testid: "GetUserLocalTimeSuccess",
    status: timeSuccess.successCount > 0 ? "success" : "fail",
    score: timeSuccess.successCount > 0 ? 1 : 0,
    "maximum marks": 1,
    message: `Get user time with valid token (${timeSuccess.successCount} successes, ${timeSuccess.networkErrorCount} network errors)`,
  });

  const timeFailure = await runTest(async () => {
    try {
      await api.getUserLocalTime("");
      throw new Error("Should have thrown MissingUserDataError");
    } catch (error) {
      if (!error.message.includes("User data not found")) throw error;
    }
  });

  testResults.data.push({
    testid: "GetUserLocalTimeFailure",
    status: timeFailure.successCount > 0 ? "success" : "fail",
    score: timeFailure.successCount > 0 ? 1 : 0,
    "maximum marks": 1,
    message: `Get user time with empty token (${timeFailure.successCount} proper error handling)`,
  });

  let errorMessageScore = 1;
  try {
    await api.authenticateUser("wrong", "credentials");
  } catch (error) {
    if (!error.message || error.message.trim().length === 0) errorMessageScore = 0;
  }

  testResults.data.push({
    testid: "ErrorMessageNonEmpty",
    status: errorMessageScore === 1 ? "success" : "fail",
    score: errorMessageScore,
    "maximum marks": 1,
    message: "Error messages are non-empty",
  });

  const outputPath = path.join("..", "evaluate.json");
  fs.writeFileSync(outputPath, JSON.stringify(testResults, null, 2));
}

runAllTests().catch(console.error);
