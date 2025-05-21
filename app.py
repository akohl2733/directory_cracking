from flask import Flask, request, jsonify
from backend.test import runner
from backend.db import insert_rec, get_connection
from flask_cors import CORS
import socket


app = Flask(__name__)
CORS(app)

@app.route("/dnscheck", methods=["GET"])
def dns_check():
    try:
        ip = socket.gethostbyname('universityscraper-server.privatelink.mysql.database.azure.com')
        return jsonify({"success": f"DNS resolved to {ip}"})
    except Exception as e:
        return jsonify({"error": str(e)})
        
@app.route('/api/store', methods=['POST'])
def store():
    data = request.json
    print(data)
    return jsonify({'status': 'success'})

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    print("Scraping url: ", url)
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

@app.route("/databases", methods=["GET"])
def list_databases():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        dbs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([db[0] for db in dbs])
    except Exception as e:
        return jsonify({"error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))