const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

async function runTests() {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      "--disable-gpu",
      "--disable-setuid-sandbox",
      "--no-sandbox",
      "--disable-dev-shm-usage",
    ],
  });

  const results = {
    data: [],
  };

  try {
    const page = await browser.newPage();

    // Test 1: Check if form submission stores data in localStorage
    const test1 = {
      testid: "LocalStorageSetImplementation",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "Failed to implement localStorage.setItem",
    };

    await page.goto("file://" + __dirname + "/index.html");

    await page.type("#firstname", "John");
    await page.type("#lastname", "Doe");
    await page.click('button[type="submit"]');

    const storedFirstname = await page.evaluate(() =>
      localStorage.getItem("firstname"),
    );
    const storedLastname = await page.evaluate(() =>
      localStorage.getItem("lastname"),
    );

    if (storedFirstname === "John" && storedLastname === "Doe") {
      test1.status = "success";
      test1.score = 1;
      test1.message = "localStorage.setItem implemented successfully";
    }
    results.data.push(test1);

    // Test 2: Check if page loads stored data from localStorage
    const test2 = {
      testid: "LocalStorageGetImplementation",
      status: "fail",
      score: 0,
      "maximum marks": 1,
      message: "Failed to implement localStorage.getItem",
    };

    const greetingText = await page.$eval("#greeting", (el) => el.textContent);
    if (greetingText === "Hello John Doe") {
      test2.status = "success";
      test2.score = 1;
      test2.message = "localStorage.getItem implemented successfully";
    }
    results.data.push(test2);
  } catch (error) {
    console.error("Error during testing:", error);
    results.data.push({
      testid: "TestError",
      status: "fail",
      score: 0,
      "maximum marks": 0,
      message: `Error during testing: ${error.message}`,
    });
  } finally {
    await browser.close();

    // Write results to evaluate.json in parent directory
    const resultPath = path.join("..", "evaluate.json");
    fs.writeFileSync(resultPath, JSON.stringify(results, null, 2));
  }
}

runTests().catch(console.error);
