document.addEventListener("DOMContentLoaded", () => {
    let addOption = document.querySelector("#add-option");
    let removeOption = document.querySelector("#remove-option");
    let optionsContainer = document.querySelector("#options-container");

    addOption.addEventListener("click", () => {
        // Create a new div element
        let div = document.createElement("div");
        // Add the classes to the div
        div.classList.add("mb-3");

        // Create a new input element
        let input = document.createElement("input");
        // Add the input's attributes and class
        input.type = "text";
        input.name = "options";
        input.classList.add("form-control");

        div.appendChild(input);
        optionsContainer.appendChild(div);
    });

    removeOption.addEventListener("click", () => {
        let options = optionsContainer.querySelectorAll("div");
        let lastOption = options[options.length - 1];

        if (options.length > 2) {
            optionsContainer.removeChild(lastOption);
        }
    });
});