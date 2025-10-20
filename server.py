from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/decoy', methods=['POST'])
def sum_numbers():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    result = num1 + num2
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
