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


    const response = { data: [] };

    try{

        // Test case 1: Filter items
        const filteredItems = await page.evaluate(() => {
            const listItems = document.querySelectorAll('#itemList li');
            return Array.from(listItems).filter(item => getComputedStyle(item).display !== 'none').length;
        });
        await page.type('#filterInput', '1');
        const filteredItems2 = await page.evaluate(() => {
            const listItems = document.querySelectorAll('#itemList li');
            return Array.from(listItems).filter(item => getComputedStyle(item).display !== 'none').length;
        });

        if (filteredItems === 3 && filteredItems2 === 2) {
            response.data.push({ testid: 1, status: 'success', score: 1,"maximum marks": 1, message: 'Filter functionality works.' });
        } else {
            response.data.push({ testid: 1, status: 'failed', score: 0,"maximum marks": 1, message: 'Filter functionality failed.' });
        }

        // Test case 2: Delete an item
        const itemsBefore = await page.evaluate(() => document.querySelectorAll('#itemList li').length);
        await page.click('#itemList .deleteBtn');
        const itemAfter = await page.evaluate(() => document.querySelectorAll('#itemList li').length);

        if (itemsBefore === itemAfter + 1) {
            response.data.push({ testid: 2, status: 'success', score: 1,"maximum marks": 1, message: 'Delete item functionality works.' });
        } else {
            response.data.push({ testid: 2, status: 'failed', score: 0,"maximum marks": 1, message: 'Delete item functionality failed.' });
        }

        // Test case 3: Clear list
        await page.click('#clearList');
        const listCleared = await page.evaluate(() => document.querySelectorAll('#itemList li').length === 0);
        if (listCleared) {
            response.data.push({ testid: 3, status: 'success', score: 1,"maximum marks": 1, message: 'Clear list functionality works.' });
        } else {
            response.data.push({ testid: 3, status: 'failed', score: 0,"maximum marks": 1, message: 'Clear list functionality failed.' });
        }

    } catch (error) {
        response.data.push({ testid: 1, status: 'error', score: 0,"maximum marks": 1, message: error });
        response.data.push({ testid: 2, status: 'error', score: 0,"maximum marks": 1, message: error });
        response.data.push({ testid: 3, status: 'error', score: 0,"maximum marks": 1, message: error });
    }

    const fs = require('fs');
    fs.writeFileSync("../evaluate.json", JSON.stringify(response, null, 2));

    await browser.close();
})();
