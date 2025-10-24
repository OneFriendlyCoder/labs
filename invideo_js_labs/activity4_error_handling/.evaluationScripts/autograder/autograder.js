const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function runTests() {
  const browser = await puppeteer.launch({
    headless: "new",
    args: [
      "--disable-gpu",
      "--disable-setuid-sandbox",
      "--no-sandbox",
      "--disable-dev-shm-usage",
    ],
  });

  const testResults = {
    data: [],
  };

  try {
    const page = await browser.newPage();

    let lastDialogMessage = "";
    page.on("dialog", async (dialog) => {
      lastDialogMessage = dialog.message();
      await dialog.accept();
    });

    await page.goto("file://" + __dirname + "/index.html");

    // Test 1: Empty name validation
    const emptyNameTest = {
      testid: "EmptyNameValidation",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "Empty name validation failed",
    };

    await page.type("#age", "20");
    await page.click('button[type="submit"]');
    const errorMessage1 = await page.$eval(
      "#errorMessage",
      (el) => el.textContent,
    );

    if (errorMessage1.includes("Name cannot be empty")) {
      emptyNameTest.status = "pass";
      emptyNameTest.score = 1;
      emptyNameTest.message = "Empty name validation implemented successfully";
    }
    testResults.data.push(emptyNameTest);

    // Test 2: Age below 18 validation
    const ageValidationTest = {
      testid: "AgeValidation",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "Age validation failed",
    };

    await page.$eval("#name", (el) => (el.value = ""));
    await page.$eval("#age", (el) => (el.value = ""));
    await page.type("#name", "John Doe");
    await page.type("#age", "15");
    await page.click('button[type="submit"]');
    const errorMessage2 = await page.$eval(
      "#errorMessage",
      (el) => el.textContent,
    );

    if (errorMessage2.includes("Age must be a number and at least 18")) {
      ageValidationTest.status = "pass";
      ageValidationTest.score = 1;
      ageValidationTest.message = "Age validation implemented successfully";
    }
    testResults.data.push(ageValidationTest);

  } catch (error) {
    console.error("Test execution error:", error);
    testResults.data.push({
      testid: "TestExecutionError",
      status: "fail",
      score: 0,
      "maximum marks": 0,
      message: `Test execution failed: ${error.message}`,
    });
  } finally {
    await browser.close();
  }

  // Write results to evaluate.json
  fs.writeFileSync(
    path.join("..", "evaluate.json"),
    JSON.stringify(testResults, null, 2),
  );
}

runTests().catch(console.error);
