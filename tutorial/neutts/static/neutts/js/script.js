const modeSelect = document.getElementById('id_mode');
const emotionalFields = document.getElementById('emotional-fields');
const cloningFields = document.getElementById('cloning-fields');
const form = document.getElementById('neutts-form');
const submitBtn = document.getElementById('submit-btn');
const btnSpinner = document.getElementById('btn-spinner');
const btnText = document.getElementById('btn-text');

function toggleFields() {
    if (modeSelect.value === 'emotional') {
        emotionalFields.style.display = 'grid';
        cloningFields.style.display = 'none';
    } else {
        emotionalFields.style.display = 'none';
        cloningFields.style.display = 'block';
    }
}

modeSelect.addEventListener('change', toggleFields);
toggleFields();

form.addEventListener('submit', function () {
    submitBtn.disabled = true;
    btnSpinner.style.display = 'inline-block';
    btnText.innerText = 'Génération en cours (IA locale)...';
});