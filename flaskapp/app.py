from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__); CORS(app)
@app.route('/analyze/<path:text>')
def analyze(text):
    sentiment = 'positive' if any(w in text.lower() for w in ['fantastic','excellent','good','great']) else 'negative'
    return jsonify({'sentiment': sentiment})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
