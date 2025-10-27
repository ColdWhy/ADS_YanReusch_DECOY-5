from flask import Flask, request, jsonify
from flask_cors import CORS
import Encryption as en

app = Flask(__name__)
CORS(app)

@app.route('/decoy', methods=['POST'])
def server_encrypt():
    data = request.get_json()
    '''
    num1 = data.get('num1')
    num2 = data.get('num2')
    
    result = num1 + num2
    
    return jsonify({'result': result})
    '''

    key = data.get('key')
    alphabet = data.get('alphabet')
    choice_stored_table = data.get('choice_stored_table')
    plaintext = data.get('plaintext')

    ciphertext = en.request_encryption(key, alphabet, choice_stored_table, plaintext)

    return jsonify({'ciphertext': ciphertext})


if __name__ == '__main__':
    app.run(debug=True)
