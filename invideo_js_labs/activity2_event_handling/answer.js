// Function to change color
function changeColor() {
    const colorBox = document.querySelector('.color-box');
    colorBox.style.backgroundColor = 'lightblue'; // Change to any color you prefer
}

// Add event listener to trigger the changeColor function on button click
document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('changeColorButton');
    button.addEventListener('click', changeColor);
});
