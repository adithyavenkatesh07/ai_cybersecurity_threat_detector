from flask import Blueprint, request, jsonify
from model.transformer_model import ThreatDetectionModel
from backend.utils.url_analyzer import URLAnalyzer
from backend.utils.feature_extractor import FeatureExtractor
from backend.utils.visualizations import get_model_metrics, generate_visualization_data

scanner_bp = Blueprint('scanner', __name__)

# Initialize components
analyzer = URLAnalyzer()
extractor = FeatureExtractor()
model = ThreatDetectionModel()

@scanner_bp.route('/scan', methods=['POST'])
def scan_url():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Analyze URL
        url_features = analyzer.analyze(url)
        
        # Extract features
        features = extractor.extract(url, url_features)
        
        # Predict threat
        prediction = model.predict(features)
        
        response = {
            'url': url,
            'is_safe': prediction['is_safe'],
            'threat_score': prediction['threat_score'],
            'threat_level': prediction['threat_level'],
            'anomalies': prediction['anomalies'],
            'details': url_features,
            'recommendations': get_recommendations(prediction),
            'visualizations': generate_visualization_data(url_features)
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scanner_bp.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        metrics_data = get_model_metrics()
        return jsonify(metrics_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_recommendations(prediction):
    recommendations = []
    
    if prediction['threat_level'] in ['MEDIUM', 'HIGH']:
        recommendations.append("⚠️ Do not enter personal information on this website")
        recommendations.append("🚫 Avoid downloading files from this source")

        
    for anomaly in prediction['anomalies']:
        if 'SSL' in anomaly:
            recommendations.append("🔒 This site lacks proper SSL encryption")
        elif 'phishing' in anomaly.lower():
            recommendations.append("🎣 Potential phishing attempt detected")
        elif 'malware' in anomaly.lower():
            recommendations.append("🦠 Possible malware distribution detected")
            
    if prediction['is_safe']:
        recommendations.append("✅ Website appears safe to visit")
        recommendations.append("💡 Always verify URLs before entering sensitive data")
    
    return recommendations
