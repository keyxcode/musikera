if (!localStorage.getItem("composerType")) {
    localStorage.setItem("composerType", "composer");
} 
if (!localStorage.getItem("epochType")) {
    localStorage.setItem("epochType", "epoch");
} 
if (!localStorage.getItem("genreType")) {
    localStorage.setItem("genreType", "genre");
} 

document.addEventListener('DOMContentLoaded', () => {
    // Load local Composer and Genre filters and show the according composers
    document.querySelector('#composer-type').value = localStorage.getItem("composerType");
    document.querySelector('#genre-type').value = localStorage.getItem("genreType");
    showComposers(localStorage.getItem("composerType"), localStorage.getItem("genreType"));
    
    // Listen to changes
    document.querySelector('#composer-type').addEventListener('change', function() {
        showComposers(this.value, localStorage.getItem("genreType"));
    })
    document.querySelector('#genre-type').addEventListener('change', function() {
        showComposers(localStorage.getItem("composerType"), this.value);
    })

    // Load local Epoch filter, show the according epochs and listen to changes
    document.querySelector('#epoch-type').value = localStorage.getItem("epochType");
    showEpoch(localStorage.getItem("epochType"));
    document.querySelector('#epoch-type').addEventListener('change', function() {
        showEpoch(this.value);
    })

    // Reset button
    document.querySelector("#reset-filters").addEventListener("click", () => {
        showComposers("composer", "genre");
        showEpoch("epoch");
    })
})

function showComposers(composerType, genreType) {
    document.querySelectorAll(".composer").forEach(e => {
        if (e.classList.contains(composerType) && e.classList.contains(genreType)) {
            e.classList.add("d-flex")
            e.classList.remove("d-none")
        } else {
            e.classList.remove("d-flex")
            e.classList.add("d-none")
        }
    })

    showMessageIfNone();

    localStorage.setItem("composerType", composerType);
    document.querySelector('#composer-type').value = localStorage.getItem("composerType");

    localStorage.setItem("genreType", genreType);
    document.querySelector('#genre-type').value = localStorage.getItem("genreType");
}

function showEpoch(epochType) {
    document.querySelectorAll(".epoch").forEach(e => {
        if (e.classList.contains(epochType)) {
            e.classList.add("d-block")
            e.classList.remove("d-none")
        } else {
            e.classList.remove("d-block")
            e.classList.add("d-none")
        }
    })

    localStorage.setItem("epochType", epochType);
    document.querySelector('#epoch-type').value = localStorage.getItem("epochType");
}

function showMessageIfNone() {
    document.querySelectorAll(".epoch").forEach(e => {
        const epochComposers = Array.from(e.querySelectorAll(".composer"));
        const allEpochComposersAreHidden = epochComposers.every(composer => composer.classList.contains("d-none"));

        if (allEpochComposersAreHidden) {
            e.querySelector(".epoch-none-message").classList.remove("d-none");
        } else {
            e.querySelector(".epoch-none-message").classList.add("d-none");
        }
    })
}