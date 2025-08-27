## Change the fucking PS

## **Problem Statement: Fixed vs. Liquid Layout Styling Challenge**

### **Objective**

Your task is to apply **CSS styling** to complete the design of two webpage sections:

1. **Fixed-width layout**
2. **Liquid (fluid) layout**

You will be provided with a partially completed CSS file (`styles.css`) containing empty **declaration blocks** for specific elements. Your job is to fill in these declaration blocks **only where instructed**, using the correct property values for widths, backgrounds, borders, padding, alignment, and font weight as described in the provided requirements.

The goal is to help you understand:

* How **fixed-width layouts** behave across different screen sizes.
* How **liquid layouts** adjust fluidly with viewport changes.
* Correct usage of CSS selectors and declaration blocks.
* Applying precise values for **colors, units, and measurements**.

---

### **Task Details**

In the provided `styles.css` file, locate the **commented TODO sections** within each selector’s declaration block for:

* `.fixed-demo .container`
* `.fixed-demo .fixed-header`
* `.fixed-demo .fixed-footer`
* `.liquid-demo .container`
* `.liquid-demo .liquid-header`
* `.liquid-demo .liquid-footer`

Each TODO contains:

* **Instructions** for what properties to add (e.g., width, background color, border, padding, text alignment, font weight).
* The **exact values** that need to be applied.

You must replace the placeholder `content: '';` inside these declaration blocks with **valid CSS declarations** according to the instructions.

---

### **Rules**

1. **Do not modify anything outside the specified declaration blocks.**
2. **Do not remove or change selectors** — they must remain exactly as provided.
3. Use the **exact values** mentioned (colors, sizes, units). Spelling or unit mistakes will cause automated tests to fail.
4. Do not remove the comments — they guide you and indicate which section to edit.
5. Maintain proper CSS syntax (property: value;).

---

### **Submission Format**

You must submit:

* A single CSS file: `styles.css`
* This file should contain all required changes within the given declaration blocks.
* No extra files, comments, or code changes outside the allowed areas.

---

### **Guidance**

* **Fixed-width layout** means the container’s width stays constant (in pixels) regardless of screen size.
* **Liquid (fluid) layout** means the container’s width is set in percentages and adapts to the viewport.
* Use the correct **color codes** (e.g., `#fffbe6` not just `yellow`).
* Border declarations can be done using shorthand (`border: 2px solid #e6d67a;`) or individual properties.
* Padding and font-weight values must match exactly what is specified.
* Once done, resize your browser window to see the difference between fixed and liquid layouts.

---

Your final CSS will be evaluated automatically. If even one value is incorrect, the related test will fail. Accuracy is key!
