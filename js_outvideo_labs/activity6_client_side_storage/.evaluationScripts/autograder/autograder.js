const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const tests = [];
let totalScore = 0;
const maxScore = 5;

async function runTest(testId, description, testFn, maxMarks) {
  try {
    await testFn();
    tests.push({
      testid: testId,
      status: "success",
      score: maxMarks,
      "maximum marks": maxMarks,
      message: `${description} - Test Passed`,
    });
    totalScore += maxMarks;
  } catch (error) {
    tests.push({
      testid: testId,
      status: "fail",
      score: 0,
      "maximum marks": maxMarks,
      message: `${description} - Test Failed: ${error.message}`,
    });
  }
}

async function autoGrade() {
  const browser = await puppeteer.launch({
    headless: "new",
    args: [
      "--disable-gpu",
      "--disable-setuid-sandbox",
      "--no-sandbox",
      "--disable-dev-shm-usage",
    ],
  });
  const page = await browser.newPage();

  try {
    await page.goto("file://" + __dirname + "/index.html", {
      waitUntil: "networkidle0",
    });
  } catch (error) {
    console.error("Failed to load page:", error);
    await browser.close();
    return;
  }

  await runTest("GetNotesInit", "getNotes initialization", async () => {
    const notes = await page.evaluate(() => getNotes());
    if (!Array.isArray(notes)) throw new Error("getNotes should return an array");
  }, 1);

  await runTest("AddNote", "Adding a new note", async () => {
    await page.type("#title", "Test Title");
    await page.type("#body", "Test Body");
    await page.click('button[onclick="addNote()"]');

    const notes = await page.evaluate(() => JSON.parse(localStorage.getItem("notes")));
    if (
      !notes ||
      notes.length !== 1 ||
      notes[0].title !== "Test Title" ||
      notes[0].body !== "Test Body"
    ) {
      throw new Error("Note was not added correctly");
    }
  }, 1);

  await runTest("DisplayNotes", "Displaying notes in the DOM", async () => {
    const noteElements = await page.$$(".note");
    if (noteElements.length !== 1)
      throw new Error("Note is not displayed correctly in DOM");

    const titleText = await page.$eval(".note h3", el => el.textContent);
    const bodyText = await page.$eval(".note p", el => el.textContent);

    if (titleText !== "Test Title" || bodyText !== "Test Body")
      throw new Error("Note content is not displayed correctly");
  }, 1);

  await runTest("DeleteNote", "Deleting a note", async () => {
    await page.click(".note button");

    const notes = await page.evaluate(() => JSON.parse(localStorage.getItem("notes")));
    if (notes.length !== 0) throw new Error("Note was not deleted correctly");

    const noteElements = await page.$$(".note");
    if (noteElements.length !== 0)
      throw new Error("Note is still displayed in DOM after deletion");
  }, 1);

  await runTest("Validation", "Input validation", async () => {
    const dialogPromise = new Promise(resolve => {
      page.on("dialog", async dialog => {
        await dialog.accept();
        resolve(true);
      });
    });

    await page.evaluate(() => {
      document.getElementById("title").value = "";
      document.getElementById("body").value = "";
    });

    await page.click('button[onclick="addNote()"]');

    const dialogShown = await Promise.race([
      dialogPromise,
      new Promise(resolve => setTimeout(() => resolve(false), 500)),
    ]);

    if (!dialogShown) throw new Error("Alert not shown for empty fields");

    const notes = await page.evaluate(() => JSON.parse(localStorage.getItem("notes")));
    if (notes.length !== 0) throw new Error("Empty note was incorrectly added");
  }, 1);

  await browser.close();

  const results = { data: tests };
  fs.writeFileSync(path.join("..", "evaluate.json"), JSON.stringify(results, null, 2));

  console.log(`Testing completed. Total score: ${totalScore}/${maxScore}`);
}

autoGrade().catch(console.error);
