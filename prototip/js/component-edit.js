// Autor: Marko Ćirić
let specIdCounter = 10;
let priceIdCounter = 10;

document.addEventListener('DOMContentLoaded', function () {
    setupImageUpload();
    setupFormSubmit();
});

function addSpec() {
    const editor = document.getElementById('specsEditor');
    specIdCounter++;
    const row = document.createElement('div');
    row.className = 'spec-row';
    row.dataset.id = specIdCounter;
    row.innerHTML = `
        <input type="text" class="spec-key" placeholder="Naziv specifikacije">
        <input type="text" class="spec-value" placeholder="Vrednost">
        <button type="button" class="spec-remove-btn" onclick="removeSpec(this)"><i class="fas fa-times"></i></button>
    `;
    editor.appendChild(row);
    row.querySelector('.spec-key').focus();
}

function removeSpec(btn) {
    btn.closest('.spec-row').remove();
}

function addPrice() {
    const editor = document.getElementById('pricesEditor');
    priceIdCounter++;
    const row = document.createElement('div');
    row.className = 'price-row';
    row.dataset.id = priceIdCounter;
    row.innerHTML = `
        <input type="text" class="store-name-input" placeholder="Naziv prodavnice" required>
        <input type="text" class="store-link-input" placeholder="Link ka prodavnici" required>
        <input type="number" class="store-price-input" placeholder="Cena u RSD" required>
        <button type="button" class="spec-remove-btn" onclick="removePrice(this)"><i class="fas fa-times"></i></button>
    `;
    editor.appendChild(row);
    row.querySelector('.store-name-input').focus();
}

function removePrice(btn) {
    btn.closest('.price-row').remove();
}

function setupImageUpload() {
    const zone = document.getElementById('imageUploadZone');
    const fileInput = document.getElementById('imageFileInput');
    const preview = document.getElementById('currentImagePreview');

    zone.addEventListener('click', () => fileInput.click());

    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.borderColor = 'var(--accent-color)';
        zone.style.backgroundColor = 'rgba(52, 152, 219, 0.08)';
    });

    zone.addEventListener('dragleave', () => {
        zone.style.borderColor = '';
        zone.style.backgroundColor = '';
    });

    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.borderColor = '';
        zone.style.backgroundColor = '';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) loadImagePreview(file, preview);
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files[0]) loadImagePreview(fileInput.files[0], preview);
    });
}

function loadImagePreview(file, imgElement) {
    const reader = new FileReader();
    reader.onload = (e) => {
        imgElement.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

function setupFormSubmit() {
    const form = document.getElementById('componentEditForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = document.getElementById('componentName').value.trim();
        if (!name) {
            alert('Molimo unesite naziv komponente.');
            return;
        }

        // In a real app, collect all data and send to backend
        const specs = [];
        document.querySelectorAll('.spec-row').forEach(row => {
            const key = row.querySelector('.spec-key').value.trim();
            const val = row.querySelector('.spec-value').value.trim();
            if (key && val) specs.push({ key, val });
        });

        const prices = [];
        document.querySelectorAll('.price-row').forEach(row => {
            const store = row.querySelector('.store-name-input').value.trim();
            const link = row.querySelector('.store-link-input').value.trim();
            const price = row.querySelector('.store-price-input').value.trim();
            if (store && price) prices.push({ store, link, price });
        });

        if (prices.length == 0) {
            alert('Mora postojati barem jedna prodavnica po komponenti!');
            return;
        }

        console.log('Component updated:', {
            name,
            category: document.getElementById('componentCategory').value,
            manufacturer: document.getElementById('componentManufacturer').value,
            description: document.getElementById('componentDescription').value,
            specs,
            prices,
        });

        alert('Izmene su uspešno sačuvane!');
        window.location.href = 'component-detail.html';
    });
}