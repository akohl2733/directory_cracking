cat > /tmp/minflask.py <<'PY'
from flask import Flask
app = Flask(__name__)
@app.route('/')
def i(): return "ok"
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
PY
python3 /tmp/minflask.py
# then in another shell:
curl http://127.0.0.1:5001/