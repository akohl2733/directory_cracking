from flask import Flask, request, jsonify
from test import runner
from db import insert_rec
app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    results = runner(url)
    return jsonify(results)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json.get('entries', [])
    for entry in data:
        insert_rec(entry)  # insert each into Azure SQL
    return jsonify({"status": "success"})