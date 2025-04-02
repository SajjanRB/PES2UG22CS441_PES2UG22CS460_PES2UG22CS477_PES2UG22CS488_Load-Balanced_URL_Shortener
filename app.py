from flask import Flask, request, redirect, jsonify
import redis
import random
import string
import os

# Initialize Flask app
app = Flask(__name__)

# Redis connection using environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
db = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, socket_timeout=5)

def generate_short_code():
    """Generates a unique 6-character short code."""
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not db.exists(short_code):  # Ensure uniqueness
            return short_code

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Accepts a long URL, generates a short URL, and stores it in Redis."""
    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    db.set(short_code, long_url)
    
    return jsonify({"short_url": f"http://localhost:5000/{short_code}"})

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirects the user from a short URL to the original long URL."""
    long_url = db.get(short_code)
    if long_url:
        return redirect(long_url)
    
    return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
