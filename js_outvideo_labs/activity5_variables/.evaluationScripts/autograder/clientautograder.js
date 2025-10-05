const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--disable-gpu', '--disable-setuid-sandbox', '--no-sandbox', '--disable-dev-shm-usage'],
        ignoreHTTPSErrors: true,
        dumpio: false
    });
    const page = await browser.newPage();

    await page.goto('file:///home/labDirectory/index.html');

    // Test cases for variables lab
    const testCases = [
        {
            testid: 1,
            description: "Task 1: City declared with var",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('City: Mumbai');
                });
                return output;
            }
        },
        {
            testid: 2,
            description: "Task 1: Temperature declared with let",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Temperature: 30');
                });
                return output;
            }
        },
        {
            testid: 3,
            description: "Task 1: Country declared with const",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Country: India');
                });
                return output;
            }
        },
        {
            testid: 4,
            description: "Task 2: Temperature can be reassigned",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Updated Temperature: 35');
                });
                return output;
            }
        },
        {
            testid: 5,
            description: "Task 3: Correct addition of num1 and num2",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Addition: 12');
                });
                return output;
            }
        },
        {
            testid: 6,
            description: "Task 3: Correct subtraction of num1 and num2",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Subtraction: 4');
                });
                return output;
            }
        },
        {
            testid: 7,
            description: "Task 4: Full Name Concatenation",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Full Name: John Doe');
                });
                return output;
            }
        },
        {
            testid: 8,
            description: "Task 5: Favorite Color Initially Set",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Original Favorite Color: blue');
                });
                return output;
            }
        },
        {
            testid: 9,
            description: "Task 5: Favorite Color Reassigned",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Updated Favorite Color: green');
                });
                return output;
            }
        },
        {
            testid: 10,
            description: "Task 7: Camel Case Conversion",
            check: async () => {
                const output = await page.evaluate(() => {
                    return document.getElementById('output').innerHTML.includes('Camel Case: firstNameOfTheUser');
                });
                return output;
            }
        }
    ];

    // Initialize response object
    const response = { "data": [] };

    // Run through test cases
    for (const testCase of testCases) {
        try {
            const passed = await testCase.check();

            response.data.push({
                "testid": testCase.testid,
                "status": passed ? "success" : "failure",
                "score": passed ? 1 : 0,
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

    // Write results to file
    const dictstring = JSON.stringify(response, null, 2);
    await fs.promises.writeFile("../evaluate.json", dictstring);

    await browser.close();
})();