from flask import Flask, request, jsonify
from flask_cors import CORS
import Encryption as en
import Decryption as de

app = Flask(__name__)
CORS(app)

@app.route('/encrypt', methods=['POST'])
def server_encrypt():
    data = request.get_json()
    key = data.get('key')
    alphabet = data.get('alphabet')
    choice_stored_table = data.get('choice_stored_table')
    choice_save_table = data.get('choice_save_table')
    plaintext = data.get('plaintext')

    ciphertext = en.request_encryption(key, alphabet, choice_stored_table, choice_save_table, plaintext)
    return jsonify({'ciphertext': ciphertext})


@app.route('/decrypt', methods=['POST'])
def server_decrypt():
    data = request.get_json()
    key = data.get('key')
    alphabet = data.get('alphabet')
    choice_stored_table = data.get('choice_stored_table')
    choice_save_table = data.get('choice_save_table')
    ciphertext = data.get('ciphertext')

    plaintext = de.request_decryption(key, alphabet, choice_stored_table, choice_save_table, ciphertext)
    return jsonify({'plaintext': plaintext})


if __name__ == '__main__':
    app.run(debug=True)
