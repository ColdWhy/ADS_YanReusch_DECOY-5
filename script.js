async function server_encrypt() {
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
    document.getElementById('encrypted_text').textContent = 'Encrypted text: (' + data.ciphertext + ')';
}

async function server_decrypt() {
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
    document.getElementById('decrypted_text').textContent = 'Decrypted text: (' + data.plaintext + ')';
}
