
document.addEventListener("DOMContentLoaded", function () {
    console.log("FloodWatch AI dashboard loaded!");
    console.log("Chart.js status:", typeof Chart);

    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

    if (typeof Chart === "undefined") {
        alert("Chart.js did not load. Please check your internet connection.");
        return;
    }

    createRainfallChart(
        "rainfallChart",
        days,
        [20, 35, 25, 60, 45]
    );

    createRiverChart(
        "riverChart",
        days,
        [2.1, 2.4, 2.2, 3.1, 2.8]
    );
});
