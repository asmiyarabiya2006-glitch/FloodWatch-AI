
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", function (event) {
        const rainfall = Number(form.elements["rainfall"].value);

        if (!Number.isFinite(rainfall) || rainfall < 0) {
            event.preventDefault();
            alert("Please enter a valid rainfall value.");
            return;
        }

        const waterLevel = form.elements["water_level"];

        if (waterLevel && waterLevel.value !== "" &&
            Number(waterLevel.value) < 0) {
            event.preventDefault();
            alert("Water level cannot be negative.");
        }
    });
});
