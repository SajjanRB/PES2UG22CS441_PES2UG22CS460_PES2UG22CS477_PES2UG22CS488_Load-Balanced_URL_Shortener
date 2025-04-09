from flask import Flask, request, redirect, jsonify
import redis
import random
import string
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")  # ✅ New!

db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_timeout=5)

def generate_short_code():
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not db.exists(short_code):
            return short_code

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    db.set(short_code, long_url)

    return jsonify({"short_url": f"{BASE_URL}/{short_code}"})  # ✅ Uses external URL now

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = db.get(short_code)
    if long_url:
        return redirect(long_url)
    return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # ✅ Binds to all interfaces
