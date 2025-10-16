from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import sys
import os

# We will launch the scraper in a subprocess to avoid blocking Flask

app = Flask(__name__)
CORS(app)

@app.route('/api/initiate-scrape', methods=['POST'])
def initiate_scrape():
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script = os.path.join(project_root, 'ScrapeSystem', 'scraper_central_nexus.py')

        # Use current python (venv) to run scraper
        python_exec = sys.executable
        subprocess.Popen([python_exec, script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"success": True, "message": "Scrape initiated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Bind explicitly to IPv4 loopback to avoid IPv6 localhost (::1) issues
    app.run(debug=True, host='127.0.0.1', port=5001)