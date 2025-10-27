async function server_encrypt() {
    const key = document.getElementById('key').value;
    const alphabet = document.getElementById('alphabet').value;
    const choice_stored_table = document.querySelector('input[name="choice"]:checked')?.value;
    plaintext = document.getElementById('plaintext').value;


    const response = await fetch('http://127.0.0.1:5000/decoy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, alphabet, choice_stored_table, plaintext })
    });

    const data = await response.json();
    document.getElementById('encrypted_text').textContent = 'Encrypted text: (' + data.ciphertext + ')';
}
