document.addEventListener('DOMContentLoaded', () => {
    // Set work filter to default
    window.addEventListener('load', () => {
        document.querySelector('#select-works').selectedIndex = "0";
    })
    
    // Work filter
    document.querySelector('#select-works').addEventListener('change', function() {
        showWorks(this.value);
    })

    // Discover work button
    document.querySelector('#discover-work').addEventListener('click', () => {
        showRandomWork();
    })
})

function showWorks(workType) {
    showAllGenreDivs();
    showCollapsableWorkList();
    filterWorksByClass(workType);
    hideGenreDivIfEmpty();
    showMessageIfNone(workType);
}

function showAllGenreDivs() {
    document.querySelectorAll(".genre-div").forEach(e => {
        e.classList.add("d-block")
        e.classList.remove("d-none")
    })
}

function showCollapsableWorkList() {
    document.querySelectorAll(".works").forEach(e => {
        e.classList.add("show");
    })
}

function filterWorksByClass(workType) {
    document.querySelectorAll(".work").forEach(e => {
        if (e.classList.contains(`${workType}`)) {
            e.classList.add("d-block")
            e.classList.remove("d-none")
        } else {
            e.classList.remove("d-block")
            e.classList.add("d-none")
        }
    })
}

function hideGenreDivIfEmpty() {
    document.querySelectorAll(".works").forEach(e => {
        const genreId = e.dataset.genre;
        const parentDiv = document.querySelector(`#div-${genreId}`);

        if (e.getBoundingClientRect()["height"] === 0) {
            parentDiv.classList.add("d-none")
            parentDiv.classList.remove("d-block")
        }
    })
}

function showMessageIfNone(workType) {
    const parentDivs = Array.from(document.querySelectorAll(".genre-div"))
    const allHidden = parentDivs.every(e => e.classList.contains("d-none"))

    const messageDiv = document.querySelector("#message");
    const workTypeSpan = document.querySelector("#work-type")

    if (allHidden) {
        messageDiv.classList.add("d-block");
        messageDiv.classList.remove("d-none");
        workTypeSpan.innerHTML = workType;
    } else {
        messageDiv.classList.remove("d-block");
        messageDiv.classList.add("d-none");
    }
}

function showRandomWork() {
    // Clear any previous random-work 
    document.querySelectorAll(".random-work").forEach(e => {
        e.classList.remove("random-work");
    })
    document.querySelector("#select-works").selectedIndex = 0;

    // Pick a random genre
    let genresAvail = []
    document.querySelectorAll(".works").forEach(e => {
        genresAvail.push(e.dataset.genre);
    })
    const numGenres = genresAvail.length;
    const randomGenreId = genresAvail[Math.floor(Math.random() * numGenres)];

    // Pick the random work from the random genre
    const randomWorksList = document.querySelector(`#collapse-${randomGenreId}`);
    const numWorks = randomWorksList.children.length;
    const randomWorkId = Math.floor(Math.random() * numWorks);

    // Add a random-work class to a work, and show it only
    randomWorksList.children.item(randomWorkId).classList.add("random-work");
    showWorks("random-work");
}