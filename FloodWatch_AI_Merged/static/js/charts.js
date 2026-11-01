console.log("FloodWatch AI charts module loaded.");

function createRainfallChart(canvasId, labels, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === "undefined") return;

    new Chart(canvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Rainfall (mm)",
                data: data,
                borderColor: "#0284c7",
                backgroundColor: "rgba(2, 132, 199, 0.15)",
                fill: true,
                tension: 0.3
            }]
        },
        options: { responsive: true }
    });
}

function createRiverChart(canvasId, labels, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === "undefined") return;

    new Chart(canvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "River Water Level (m)",
                data: data,
                borderColor: "#16a34a",
                backgroundColor: "rgba(22, 163, 74, 0.15)",
                fill: true,
                tension: 0.3
            }]
        },
        options: { responsive: true }
    });
}