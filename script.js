function showLoader() {
    document.querySelectorAll(".glow").forEach(g => g.classList.add("visible"));
}

function hideLoader() {
    document.querySelectorAll(".glow").forEach(g => g.classList.remove("visible"));
}

async function server_encrypt() {
    showLoader();

    const key = document.getElementById('key').value;
    const alphabet = document.getElementById('alphabet').value;
    const choice_stored_table = document.querySelector('input[name="choice"]:checked')?.value;
    const choice_save_table = document.querySelector('input[name="save_choice"]:checked')?.value;
    const plaintext = document.getElementById('plaintext').value;

    const response = await fetch('http://127.0.0.1:5000/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, alphabet, choice_stored_table, choice_save_table, plaintext })
    });

    const data = await response.json();
    document.getElementById('output_en').textContent = "OUTPUT";
    document.getElementById('encrypted_text').textContent = data.ciphertext;

    hideLoader();
}

async function server_decrypt() {
    showLoader();

    const key = document.getElementById('key').value;
    const alphabet = document.getElementById('alphabet').value;
    const choice_stored_table = document.querySelector('input[name="choice"]:checked')?.value;
    const choice_save_table = document.querySelector('input[name="save_choice"]:checked')?.value;
    const ciphertext = document.getElementById('ciphertext').value;

    const response = await fetch('http://127.0.0.1:5000/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, alphabet, choice_stored_table, choice_save_table, ciphertext })
    });

    const data = await response.json();
    document.getElementById('output_de').textContent = "OUTPUT";
    document.getElementById('decrypted_text').textContent = data.plaintext;

    hideLoader();
}
