Objective  
Your task is to apply CSS Grid alignment properties to complete the design of several webpage sections.  

You will be provided with a partially completed CSS file (`styles.css`) containing empty declaration blocks (`content: '';`) for specific selectors. Your job is to fill in these declaration blocks only where instructed, using the correct alignment property values as described in the provided requirements.  

The goal is to help you understand:  

How **align-content** distributes rows vertically inside a grid.  
How **align-items** aligns items vertically within their own cells.  
How **justify-content** distributes columns horizontally inside a grid container.  
How **justify-items** aligns items horizontally inside their own cells.  
The difference between **grid-level track alignment** vs **item-level alignment**.  


Task Details :
In the provided `styles.css` file, locate the commented TODO sections within each selector’s declaration block for:  

`.align-content-start`  
`.align-content-space-around`  
`.align-items-start`  
`.align-items-end`  
`.justify-content-end`  
`.justify-content-space-evenly`  
`.justify-items-center`  
`.justify-items-end`  

Each TODO contains :  
Instructions for what alignment property to add (e.g., `align-content`, `justify-items`).  
The exact value that needs to be applied (e.g., `start`, `end`, `space-around`, `center`).  
You must replace the placeholder `content: '';` inside these declaration blocks with valid CSS declarations according to the instructions.  


Rules 
1. Do not modify anything outside the specified declaration blocks.  
2. Do not remove or rename selectors — they must remain exactly as provided.  
3. Use the exact property names and values indicated in the TODO instructions. Spelling mistakes will cause automated tests to fail, so avoid them.  
4. Do not remove the comments — they guide you and indicate which section to edit.  
5. Maintain proper CSS syntax (`property: value;`).  


Submission Format : 
A single CSS file: `css/styles.css`  
This file should contain all required changes within the given declaration blocks.  
No extra files, comments, or code changes outside the allowed areas.  


Guidance  

`align-content` → controls distribution of the whole grid’s rows along the block (vertical) axis.  
`align-items` → controls alignment of items inside their own cells vertically.  
`justify-content` → controls distribution of the grid’s columns along the inline (horizontal) axis.  
`justify-items` → controls alignment of items inside their own cells horizontally.  
Resize your browser or stretch the demo containers to see the visual differences.  
