const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        headless: true
    });
    const page = await browser.newPage();
    
    await page.goto('file:///home/labDirectory/index.html');

    const testCases = [
        {
            testid: 1,
            description: "Name is John",
            check: async () => {
                return await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Name: John');
                });
            }
        },
        {
            testid: 2,
            description: "Age is 20",
            check: async () => {
                return await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Age: 20');
                });
            }
        },
        {
            testid: 3,
            description: "isStudent is true",
            check: async () => {
                return await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Is Student: true');
                });
            }
        }
    ];

    const response = { "data": [] };
    let totalScore = 0;

    for (const testCase of testCases) {
        try {
            const passed = await testCase.check();
            const score = passed ? 1 : 0;
            totalScore += score;

            response.data.push({
                "testid": testCase.testid,
                "status": passed ? "success" : "failure",
                "score": score,
                "maximum marks": 1,
                "message": passed 
                    ? `Passed: ${testCase.description}` 
                    : `Failed: ${testCase.description}`
            });
        } catch (error) {
            response.data.push({
                "testid": testCase.testid,
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": `Test failed: ${error.message}`
            });
        }
    }

    // Add total score to response
    response.totalScore = totalScore;
    response.maxScore = testCases.length;

    // Write results to file
    await fs.promises.writeFile("../evaluate.json", JSON.stringify(response, null, 2));

    await browser.close();
})();