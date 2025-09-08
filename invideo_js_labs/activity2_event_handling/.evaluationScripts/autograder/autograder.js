const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--disable-gpu', '--disable-setuid-sandbox', '--no-sandbox', '--disable-dev-shm-usage'],
        ignoreHTTPSErrors: true,
        dumpio: false
    });
    const page = await browser.newPage();

    // Load the student's HTML file
    await page.goto('file://' + __dirname + '/index.html');

    // Initialize response object
    const response = { "data": [] };

    try {
        // Wait for the button and color box to load
        await page.waitForSelector('#changeColorButton');
        await page.waitForSelector('.color-box');

        // Check initial color
        const initialColor = await page.$eval('.color-box', el => window.getComputedStyle(el).backgroundColor);

        // Click the button
        await page.click('#changeColorButton');
        await new Promise(resolve => setTimeout(resolve, 500)); // Give time for color change

        // Check if color changed
        const newColor = await page.$eval('.color-box', el => window.getComputedStyle(el).backgroundColor);
        if (newColor === 'rgb(173, 216, 230)' && initialColor === 'rgb(128, 128, 128)') {
            response.data.push({
                "testid": 1,
                "status": "success",
                "score": 1,
                "maximum marks": 1,
                "message": "Color changed to lightblue when button was clicked."
            });
        } else if (newColor === 'rgb(173, 216, 230)'){
            response.data.push({
                "testid": 1,
                "status": "failed",
                "score": 0.5,
                "maximum marks": 1,
                "message": "Color was lightblue when button was clicked, but the initial color was not gray."
            });
        }
        else{
            response.data.push({
                "testid": 1,
                "status": "failed",
                "score": 0,
                "maximum marks": 1,
                "message": "Color did not change as expected when button was clicked."
            });
        }

    } catch (error) {
        response.data.push({
            "testid": 1,
            "status": "failed",
            "score": 0,
            "maximum marks": 1,
            "message": error.toString()
        });
    }

    // Output results to evaluate.json
    const fs = require('fs');
    fs.writeFileSync("../evaluate.json", JSON.stringify(response, null, 2));

    await browser.close();
})();
