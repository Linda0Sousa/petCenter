const selects = document.querySelectorAll(".custom-select");

selects.forEach(select => {
    const trigger = select.querySelector(".custom-select-trigger");
    const options = select.querySelectorAll(".custom-option");

    trigger.addEventListener("click", () => {
        select.classList.toggle("open");
    });

    options.forEach(option => {
        option.addEventListener("click", () => {
            trigger.textContent = option.textContent;
            select.classList.remove("open");
        });
    });
});

document.addEventListener("click", (e) => {
    selects.forEach(select => {
        if (!select.contains(e.target)) {
            select.classList.remove("open");
        }
    });
});