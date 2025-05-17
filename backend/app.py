from flask import Flask, request, jsonify
from test import runner
from db import insert_rec
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/store', methods=['POST'])
def store():
    data = request.json
    print(data)
    return jsonify({'status': 'success'})

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    print("Scraping URL: ", url)
    if not url:
        return jsonify({'Error': "No URL provided"}), 400
    try:
        results = runner(url)
        return jsonify(results)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json.get('entries', [])
    if not data:
        return jsonify({"error": "No entries provided"}), 400
    try:
        for entry in data:
            insert_rec(entry)  # insert each into Azure SQL
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))