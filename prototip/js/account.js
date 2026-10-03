// Autor: Marko Ćirić
document.addEventListener('DOMContentLoaded', function () {
    setupDeleteModal();
});

function openDeleteModal() {
    const modal = document.getElementById('deleteAccountModal');
    modal.classList.add('show');
    document.getElementById('deleteConfirmInput').value = '';
    document.getElementById('confirmDeleteBtn').disabled = true;
}

function closeDeleteModal() {
    document.getElementById('deleteAccountModal').classList.remove('show');
}

function setupDeleteModal() {
    const input = document.getElementById('deleteConfirmInput');
    const btn = document.getElementById('confirmDeleteBtn');

    input.addEventListener('input', function () {
        btn.disabled = this.value.trim() !== 'OBRISI';
    });

    document.getElementById('deleteAccountModal').addEventListener('click', function (e) {
        if (e.target === this) closeDeleteModal();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeDeleteModal();
    });
}

function handleDeleteAccount() {
    alert('Vaš nalog je uspešno obrisan.');
    window.location.href = 'index.html';
}

function handleLogout() {
    alert('Uspešno ste se odjavili.');
    window.location.href = 'login.html';
}