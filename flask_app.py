from flask import Flask, request, jsonify
from modelisation import main

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Attend une requête POST JSON avec une clé 'url_or_id' contenant l'URL ou l'ID
    url_or_id = data['url_or_id']
    prediction = main(url_or_id)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
