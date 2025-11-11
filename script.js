let timer;
let isRunning = false;
let [hours, minutes, seconds] = [0, 0, 0];

const display = document.getElementById("display");
const startBtn = document.getElementById("start");
const pauseBtn = document.getElementById("pause");
const resetBtn = document.getElementById("reset");
const lapBtn = document.getElementById("lap");
const laps = document.getElementById("laps");

// Update the stopwatch display
function updateDisplay() {
  let h = hours < 10 ? "0" + hours : hours;
  let m = minutes < 10 ? "0" + minutes : minutes;
  let s = seconds < 10 ? "0" + seconds : seconds;
  display.innerText = `${h}:${m}:${s}`;
}

// Start function
startBtn.addEventListener("click", () => {
  if (!isRunning) {
    isRunning = true;
    timer = setInterval(() => {
      seconds++;
      if (seconds === 60) {
        seconds = 0;
        minutes++;
      }
      if (minutes === 60) {
        minutes = 0;
        hours++;
      }
      updateDisplay();
    }, 1000);
  }
});

// Pause function
pauseBtn.addEventListener("click", () => {
  clearInterval(timer);
  isRunning = false;
});

// Reset function
resetBtn.addEventListener("click", () => {
  clearInterval(timer);
  isRunning = false;
  [hours, minutes, seconds] = [0, 0, 0];
  updateDisplay();
  laps.innerHTML = "";
});

// Lap function
lapBtn.addEventListener("click", () => {
  if (isRunning) {
    let lapTime = display.innerText;
    let li = document.createElement("li");
    li.innerText = `Lap: ${lapTime}`;
    laps.appendChild(li);
  }
});

// Initialize display
updateDisplay();
