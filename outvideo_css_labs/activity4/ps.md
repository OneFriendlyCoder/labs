## **Problem Statement: Responsive Layout and Flexbox Challenge**

### **Objective**

Your task is to apply **CSS styling** to complete the design of a responsive webpage layout. The layout includes a **site header**, a **hero section**, and **content grid areas** (main article + sidebar).  

You will be provided with a partially completed CSS file (`styles.css`) containing empty **declaration blocks** for specific elements. Your job is to fill in these declaration blocks **only where instructed**, using the correct property values for **flexbox, grid alignment, responsive typography, and image scaling**.

The goal is to help you understand:

* How to use **flexbox** for header alignment and navigation layout.  
* How to create **fluid typography** with viewport-based units.  
* How to make **responsive images** that adapt to different screen sizes.  
* How to apply **max-width and scaling rules** to avoid distortion.  

---

### **Task Details**

In the provided `styles.css` file, locate the **commented TODO sections** within each selector’s declaration block for:

* `.header-inner`  
* `.hero-title`  
* `.hero-img`  
* `.responsive-img, .hero-img, .full-width-img`  
* `.maxwidth-img`  

Each TODO contains:

* **Instructions** for what properties to add (e.g., `display: flex;`, `justify-content: space-between;`, `font-size: 5vw;`, `width: 100%; height: auto;`, etc.).  
* The **exact values or units** required to achieve the intended responsive design.  

You must replace the placeholder `content: '';` inside these declaration blocks with **valid CSS declarations** according to the instructions.  

---

### **Rules**

1. **Do not modify anything outside the specified declaration blocks.**  
2. **Do not remove or rename selectors** — they must remain exactly as provided.  
3. Use the **exact property values and units** described in the instructions. Any mismatch will cause automated tests to fail.  
4. Do not remove the comments — they indicate where and how to edit.  
5. Maintain proper CSS syntax (`property: value;`).  

---

### **Submission Format**

You must submit:  

* A single CSS file: `styles.css`  
* This file should contain all required changes within the given declaration blocks.  
* No extra files, comments, or code changes outside the allowed areas.  

---

### **Guidance**

* For `.header-inner`, use **flexbox** with `display: flex;`, `align-items: center;`, `justify-content: space-between;`, and enable wrapping for smaller screens.  
* For `.hero-title`, use **viewport-based units** (`vw`) to scale text fluidly, apply a **line-height of ~1.05**, and use **max-width in characters (ch)** to limit long lines.  
* For `.hero-img` and `.responsive-img`, apply `width: 100%; height: auto; display: block;` along with subtle `border-radius`.  
* For `.maxwidth-img`, ensure images **never upscale beyond their intrinsic size** with `max-width: 100%; height: auto;`.  
* Test your design by resizing the browser window to confirm the layout and typography adjust smoothly across screen sizes.  

---

Your final CSS will be evaluated automatically. If even one value is incorrect, the related test will fail. **Precision and accuracy are critical!**
