// Timer Functionality
let progress = 0;
let progressBar = document.querySelector(".progress");

function startTimer() {
    let timer = setInterval(() => {
        if (progress < 100) {
            progress += 50;
            progressBar.style.width = progress + "%";
        } else {
            clearInterval(timer);
        }
    }, 1000);
}

// Start the timer when the page loads
window.onload = startTimer;
