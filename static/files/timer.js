// Timer Functionality
let progress = 0;
let progressBar = document.querySelector(".progress");

function startTimer() {
    progressBar.style.transition = "width 5s ease";
    progressBar.style.width = "100%";
    
    setTimeout(() => {
        document.getElementById('timedQuestionForm').submit();
    }, 5000);// 5secons change how long here
}
// Start the timer when the page loads
window.onload = startTimer;
