# File: app.py (Flask Backend)
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
    # Simulated related ASINs (in practice, use a free API or scraped result)
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
    app.run(debug=True)


// File: frontend/src/App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [inputUrl, setInputUrl] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/api/get-links", {
        url: inputUrl,
      });
      setResults(res.data.related_links);
    } catch (err) {
      alert("Error: " + err.response?.data?.error || "Unknown error");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Amazon Product Link Finder</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="text"
          placeholder="Paste Amazon product URL"
          className="border p-2 w-full"
          value={inputUrl}
          onChange={(e) => setInputUrl(e.target.value)}
        />
        <button className="mt-2 bg-blue-600 text-white px-4 py-2 rounded">
          Get Related Links
        </button>
      </form>
      {results.length > 0 && (
        <div className="bg-gray-100 p-4 rounded">
          <h2 className="font-semibold mb-2">Related Products:</h2>
          <ul className="list-disc pl-5">
            {results.map((link, index) => (
              <li key={index}>
                <a href={link} target="_blank" rel="noopener noreferrer" className="text-blue-700 underline">
                  {link}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;


// File: frontend/tailwind.config.js (Optional for styling)
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
