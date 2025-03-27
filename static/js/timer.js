// Timer Functionality
let progress = 0;
let progressBar = document.querySelector(".progress");

function startTimer() {
    progressBar.style.transition = "width 5s ease";
    progressBar.style.width = "100%";
    
    setTimeout(() => {
        window.location.href = "/quiz/finish";
    }, 5000);// 5secons change how long here
}
// Start the timer when the page loads
window.onload = startTimer;
