from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add model directory to path
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.routes.scanner import scanner_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(scanner_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Cybersecurity Threat Detector API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
