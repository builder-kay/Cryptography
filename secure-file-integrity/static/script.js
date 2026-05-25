const fileInputs = document.querySelectorAll('input[type="file"]');
const modeButtons = document.querySelectorAll(".mode-button");
const workflowPanels = document.querySelectorAll(".workflow-panel");

modeButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const targetId = button.dataset.workflowTarget;

        modeButtons.forEach((item) => item.classList.remove("is-active"));
        workflowPanels.forEach((panel) => panel.classList.remove("is-active"));

        button.classList.add("is-active");
        document.getElementById(targetId)?.classList.add("is-active");
    });
});

fileInputs.forEach((input) => {
    input.addEventListener("change", () => {
        const label = input.previousElementSibling;
        if (input.files.length > 0) {
            label.textContent = `Selected: ${input.files[0].name}`;
        }
    });
});
