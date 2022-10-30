document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-button').forEach(e => e.addEventListener('click', function() {
        toggleLikeButtonUI(e);
        
        const workID = this.dataset.work;
        const currentUser = document.querySelector('#user').innerHTML;
        updateLikeBackEnd(currentUser, workID);
    }))
})

function toggleLikeButtonUI(likeButton) {
    if (likeButton.classList.contains('liked')) {
        likeButton.classList.remove('liked');
        likeButton.innerHTML = `<i class="fa-regular fa-heart"></i>`
    } else {
        likeButton.classList.add('liked');
        likeButton.innerHTML = `<i class="fa-solid fa-heart"></i>`
    }
}

function updateLikeBackEnd(currentUser, workID) {
    fetch(`/api/work/${workID}`, {
        method: 'PUT',
        body: JSON.stringify({
            current_user: currentUser
        })
    })
}