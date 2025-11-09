import numpy as np

class FeatureExtractor:
    def extract(self, url, url_features):
        # Convert features to numerical vector
        feature_vector = [
            url_features['url_length'] / 100.0,  # Normalize
            1.0 if url_features['has_ip'] else 0.0,
            1.0 if url_features['has_suspicious_keywords'] else 0.0,
            url_features['subdomain_count'] / 5.0,  # Normalize
            1.0 if url_features['has_https'] else 0.0,
            url_features['domain_age'],
            url_features['special_char_count'] / 20.0,  # Normalize
            1.0 if url_features['has_redirect'] else 0.0
        ]
        
        return np.array(feature_vector, dtype=np.float32)