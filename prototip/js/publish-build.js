// Autor: Aleksandar Cvetković
const publishState = {
    images: [],
    benchmarks: [],
    components: [
        // Example components (in real app, these would come from backend)
        { id: 1, name: 'CPU: Intel Core i9-13900K', price: '45.000 RSD' },
        { id: 2, name: 'GPU: NVIDIA RTX 4090', price: '120.000 RSD' },
        { id: 3, name: 'RAM: Corsair Dominator Platinum 32GB', price: '12.000 RSD' },
        { id: 4, name: 'SSD: Samsung 990 Pro 2TB', price: '18.000 RSD' }
    ]
};


document.addEventListener('DOMContentLoaded', function() {
    setupImageUpload();
    setupBenchmarkTable();
    setupFormSubmission();
    displayComponents();
});


function setupImageUpload() {
    const uploadArea = document.getElementById('imageUploadArea');
    const imageInput = document.getElementById('imageInput');
    const imageErrorDiv = document.getElementById('imageError');

    uploadArea.addEventListener('click', () => imageInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.15)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';
        handleImageFiles(e.dataTransfer.files);
    });

    imageInput.addEventListener('change', (e) => {
        handleImageFiles(e.target.files);
    });
}

function handleImageFiles(files) {
    const imageErrorDiv = document.getElementById('imageError');
    const maxImages = 5;

    if (publishState.images.length + files.length > maxImages) {
        showError(imageErrorDiv, `Možete dodati maksimalno ${maxImages} slika. Trenutno ste uneli ${publishState.images.length} slika.`);
        return;
    }

    for (let file of files) {
        if (!file.type.startsWith('image/')) {
            showError(imageErrorDiv, 'Molimo dodajte samo slike.');
            continue;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            publishState.images.push({
                id: Date.now() + Math.random(),
                src: e.target.result,
                file: file
            });
            displayImagePreviews();
            clearError(imageErrorDiv);
        };
        reader.readAsDataURL(file);
    }
}

function displayImagePreviews() {
    const container = document.getElementById('imagePreviewContainer');
    container.innerHTML = '';

    publishState.images.forEach((image) => {
        const preview = document.createElement('div');
        preview.className = 'image-preview';
        preview.innerHTML = `
            <img src="${image.src}" alt="Preview">
            <button type="button" class="image-remove-btn" data-image-id="${image.id}">✕</button>
        `;

        preview.querySelector('.image-remove-btn').addEventListener('click', (e) => {
            e.preventDefault();
            publishState.images = publishState.images.filter(img => img.id !== image.id);
            displayImagePreviews();
        });

        container.appendChild(preview);
    });
}


function setupBenchmarkTable() {
    const addBtn = document.getElementById('addBenchmarkBtn');
    addBtn.addEventListener('click', addBenchmarkRow);
}

function addBenchmarkRow() {
    const benchmarkBody = document.getElementById('benchmarkBody');
    const emptyRow = benchmarkBody.querySelector('.empty-row');

    if (emptyRow) {
        emptyRow.remove();
    }

    const rowId = Date.now();
    const row = document.createElement('tr');
    row.dataset.benchmarkId = rowId;
    row.innerHTML = `
        <td><input type="text" placeholder="npr. 3DMark, GTA VI, Cinebench..." required></td>
        <td><input type="text" placeholder="npr. 60 FPS" required></td>
        <td><button type="button" class="remove-row-btn" data-row-id="${rowId}">Obriši</button></td>
    `;

    row.querySelector('.remove-row-btn').addEventListener('click', (e) => {
        e.preventDefault();
        row.remove();
        publishState.benchmarks = publishState.benchmarks.filter(b => b.id !== rowId);
        checkEmptyBenchmarkTable();
    });

    benchmarkBody.appendChild(row);
}

function checkEmptyBenchmarkTable() {
    const benchmarkBody = document.getElementById('benchmarkBody');
    const rows = benchmarkBody.querySelectorAll('tr:not(.empty-row)');

    if (rows.length === 0) {
        benchmarkBody.innerHTML = `
            <tr class="empty-row">
                <td colspan="3" class="center">Nema unetih rezultata. Klikni "Dodaj rezultat" da počneš.</td>
            </tr>
        `;
    }
}


function displayComponents() {
    const componentsList = document.getElementById('componentsList');
    componentsList.innerHTML = '';

    if (publishState.components.length === 0) {
        componentsList.innerHTML = '<p class="placeholder">Nema odabranih komponenti</p>';
        return;
    }

    publishState.components.forEach(component => {
        const componentItem = document.createElement('div');
        componentItem.className = 'component-item';
        componentItem.innerHTML = `
            <span class="component-name">${component.name}</span>
            <span class="component-price">${component.price}</span>
        `;
        componentsList.appendChild(componentItem);
    });
}


function setupFormSubmission() {
    const form = document.getElementById('publishBuildForm');
    form.addEventListener('submit', handleFormSubmit);
}

function handleFormSubmit(e) {
    e.preventDefault();

    const description = document.getElementById('description').value.trim();
    const imageErrorDiv = document.getElementById('imageError');
    const benchmarkErrorDiv = document.getElementById('benchmarkError');


    clearError(imageErrorDiv);
    clearError(benchmarkErrorDiv);


    if (!description) {
        alert('Molimo popunite opis.');
        return;
    }


    if (publishState.images.length === 0) {
        showError(imageErrorDiv, 'Molimo dodajte najmanje jednu sliku.');
        return;
    }


    const benchmarkRows = document.querySelectorAll('#benchmarkBody tr:not(.empty-row)');
    if (benchmarkRows.length === 0) {
        showError(benchmarkErrorDiv, 'Molimo dodajte najmanje jedan rezultat benchmark softvera.');
        return;
    }


    const benchmarks = [];
    benchmarkRows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        const softwareName = inputs[0].value.trim();
        const result = inputs[1].value.trim();

        if (!softwareName || !result) {
            showError(benchmarkErrorDiv, 'Molimo popunite sva polja u benchmark tabeli.');
            return;
        }

        benchmarks.push({
            software: softwareName,
            result: result
        });
    });

    if (benchmarks.length === 0) return;


    const formData = {
        description: description,
        images: publishState.images.length,
        benchmarks: benchmarks,
        components: publishState.components
    };

    console.log('Build data:', formData);


    alert('Vaš računar je uspešno objavljen!');


    window.location.href = 'index.html';

}


function showError(errorDiv, message) {
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}

function clearError(errorDiv) {
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
}

