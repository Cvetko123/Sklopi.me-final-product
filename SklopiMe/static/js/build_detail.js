// Marko Ciric 2023/0133

let BUILD_ID, RATE_URL, EDIT_URL, DELETE_URL, IS_OWNER;

document.addEventListener('DOMContentLoaded', function() {

    const dataElement = document.getElementById("build-data");
    if (!dataElement) {
        return;
    }

    BUILD_ID = dataElement.dataset.buildId;
    RATE_URL = dataElement.dataset.rateUrl;
    EDIT_URL = dataElement.dataset.editUrl;
    DELETE_URL = dataElement.dataset.deleteUrl;
    IS_OWNER = dataElement.dataset.isOwner === "true";


    setupLikes();

    if (IS_OWNER) {
        setupModals();
    }
});

function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    if (!cookieValue) {
        const carrier = document.querySelector('[name=csrfmiddlewaretoken]');
        if (carrier) cookieValue = carrier.value;
    }
    return cookieValue || '';
}

function setupModals() {
    const editBtn = document.getElementById('editBtn');
    const deleteBtn = document.getElementById('deleteBtn');

    const editModal = document.getElementById('editModal');
    const deleteModal = document.getElementById('deleteModal');


    if (editBtn) {
        editBtn.addEventListener('click', function(e) {
            e.preventDefault();

            if (editModal) {
                const titleEl = document.getElementById('buildTitle');
                const descEl = document.getElementById('buildDescription');
                if(titleEl) document.getElementById('editTitle').value = titleEl.textContent.trim();
                if(descEl) document.getElementById('editDescription').value = descEl.textContent.trim();

                editModal.style.display = 'block';
                editModal.classList.add('show');
            }
        });
    }

    if (deleteBtn) {
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (deleteModal) {
                deleteModal.style.display = 'block';
                deleteModal.classList.add('show');
            }
        });
    }

    const closeButtons = document.querySelectorAll('.close-modal, .cancel-btn');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (editModal) { editModal.style.display = 'none'; editModal.classList.remove('show'); }
            if (deleteModal) { deleteModal.style.display = 'none'; deleteModal.classList.remove('show'); }
        });
    });

    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const newTitle = document.getElementById('editTitle').value.trim();
            const newDescription = document.getElementById('editDescription').value.trim();

            fetch(EDIT_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: new URLSearchParams({ name: newTitle, description: newDescription }),
            })
            .then(response => {
                if (!response.ok) throw new Error('Izmena nije uspela');
                return response.json();
            })
            .then(data => {
                const titleEl = document.getElementById('buildTitle');
                const descEl = document.getElementById('buildDescription');
                if (titleEl) titleEl.textContent = data.name;
                if (descEl) descEl.textContent = data.description;
                if (editModal) {
                    editModal.style.display = 'none';
                    editModal.classList.remove('show');
                }
            })
            .catch(err => {
                alert('Došlo je do greške.');
            });
        });
    }

    const confirmDeleteBtn = document.querySelector('.delete-confirmation .delete-btn');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            fetch(DELETE_URL, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    window.location.href = '/builds';
                }
            })
            .catch(err => {
                alert('Došlo je do greške.');
            });
        });
    }
}

function setupLikes() {
    const likeBtn = document.getElementById('likeBtn');
    const dislikeBtn = document.getElementById('dislikeBtn');
    if (likeBtn) likeBtn.addEventListener('click', () => sendVote('like', likeBtn, dislikeBtn));
    if (dislikeBtn) dislikeBtn.addEventListener('click', () => sendVote('dislike', likeBtn, dislikeBtn));
}

function sendVote(vote, likeBtn, dislikeBtn) {
    likeBtn.disabled = true;
    dislikeBtn.disabled = true;
    fetch(RATE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify({ vote: vote }),
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById('likeCount').textContent = data.likes;
        document.getElementById('dislikeCount').textContent = data.dislikes;
        likeBtn.classList.toggle('liked', data.user_vote === 'like');
        dislikeBtn.classList.toggle('disliked', data.user_vote === 'dislike');
    })
    .catch(err => console.error(err))
    .finally(() => { likeBtn.disabled = false; dislikeBtn.disabled = false; });
}

window.changeMainImage = function(thumbnail) {
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    if (mainImage) mainImage.src = thumbnail.querySelector('img').src;
    thumbnails.forEach(t => t.classList.remove('active'));
    thumbnail.classList.add('active');
}