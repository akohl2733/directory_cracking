from flask import Flask, request, jsonify
from backend.test import runner
from backend.db import insert_rec, get_connection
from flask_cors import CORS
import socket
import os
import sys
import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'UniversityScraper backend is running!'

@app.route("/dnscheck", methods=["GET"])
def dns_check():
    try:
        ip = socket.gethostbyname('directoryscraper-mysql.mysql.database.azure.com')
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

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        entries = data.get("entries", [])
        for entry in entries:
            insert_rec(entry)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Submission error:", e)
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
    app.run(debug=True, host='0.0.0.0', port=5001)