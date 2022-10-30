document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#sort-favorites").addEventListener('change', function() {
        sortComposers(this.value);
    })
})

function sortComposers(sortType) {
    const wrapper = document.querySelector("#wrapper");
    const songDivs = Array.from(wrapper.children);
    
    const sortedSongDivs = songDivs.sort((a, b) => a.dataset[sortType].localeCompare(b.dataset[sortType]));
    
    wrapper.innerHTML = "";
    for (let sortedSongDiv of sortedSongDivs) {
        wrapper.appendChild(sortedSongDiv);
    }
}