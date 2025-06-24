# app.py (Flask Backend)
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # Enable CORS

# Extract ASIN from Amazon URL
def extract_asin(url):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    return None

# Dummy function to simulate free API for related products (returns static results)
def get_related_products(asin):
    related_asins = [
        "B07MJL8NXR", "B09VD48CX6", "B09TKLYT2T", "B095RTT889",
        "B0DHTMMY8L", "B09KQSM1X6", "B0DC8TND9X", "B0DHTN91HC"
    ]
    return [f"https://www.amazon.com/dp/{a}" for a in related_asins]

@app.route("/api/get-links", methods=["POST"])
def get_links():
    data = request.get_json()
    url = data.get("url")
    asin = extract_asin(url)
    if not asin:
        return jsonify({"error": "Invalid Amazon URL"}), 400
    related_links = get_related_products(asin)
    return jsonify({"asin": asin, "related_links": related_links})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
