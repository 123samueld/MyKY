from flask import Flask, jsonify
from scraper_central_nexus import scrapeSelectedSites

app = Flask(__name__)

@app.route('/api/initiate-scrape', methods=['POST'])
def initiate_scrape():
    try:
        # Call the specific function
        result = scrapeSelectedSites()
        return jsonify({"success": True, "message": "Scrape initiated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)