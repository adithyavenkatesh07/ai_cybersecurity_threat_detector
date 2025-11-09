import torch
import torch.nn as nn
import numpy as np

class ThreatDetectionTransformer(nn.Module):
    def __init__(self, input_dim=8, hidden_dim=128, num_heads=4, num_layers=3):
        super(ThreatDetectionTransformer, self).__init__()
        
        self.embedding = nn.Linear(input_dim, hidden_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=0.1,
            batch_first=True
        )
        
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        x = self.embedding(x)
        x = x.unsqueeze(1)  # Add sequence dimension
        x = self.transformer_encoder(x)
        x = x.squeeze(1)  # Remove sequence dimension
        output = self.classifier(x)
        return output


class ThreatDetectionModel:
    def __init__(self):
        self.model = ThreatDetectionTransformer()
        self.model.eval()
        self.threshold = 0.6  # threat_score > 0.6 considered unsafe

    def predict(self, features):
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            output = self.model(features_tensor)
            threat_score = output.item()

            # ✅ Slightly scale down ONLY for obviously safe URLs like Google
            has_https, has_ip, has_suspicious, domain_age, has_redirect = (
                features[4], features[1], features[2], features[5], features[7]
            )
            if has_https > 0.8 and has_ip < 0.1 and has_suspicious < 0.1 \
               and domain_age > 0.5 and has_redirect < 0.2:
                threat_score *= 0.5  # slight reduction for known safe URLs

        anomalies = self._detect_anomalies(features, threat_score)
        threat_level = self._calculate_threat_level(threat_score)

        # ✅ Consider unsafe if anomalies exist OR score above threshold
        is_safe = threat_score < self.threshold and len(anomalies) == 0

        return {
            'is_safe': is_safe,
            'threat_score': round(threat_score * 100, 2),
            'threat_level': threat_level,
            'anomalies': anomalies
        }

    def _detect_anomalies(self, features, threat_score):
        anomalies = []
        has_ip, has_suspicious, subdomains, has_https, domain_age, special_chars, has_redirect = (
            features[1], features[2], features[3], features[4], features[5], features[6], features[7]
        )

        if has_ip > 0.5:
            anomalies.append("IP address used instead of domain name")

        if has_suspicious > 0.5:
            anomalies.append("Contains suspicious keywords (potential phishing)")

        if subdomains > 0.8:
            anomalies.append("Too many subdomains (may be suspicious)")

        if special_chars > 0.8:
            anomalies.append("Unusual special characters in URL")

        if has_https < 0.5:
            anomalies.append("No HTTPS detected (less secure)")

        if domain_age < 0.2:
            anomalies.append("Newly registered domain")

        if has_redirect > 0.7:
            anomalies.append("Multiple redirects detected")

        if threat_score > 0.8:
            anomalies.append("High probability of malicious intent")

        return anomalies

    def _calculate_threat_level(self, score):
        if score < 0.4:
            return "LOW"
        elif score < 0.7:
            return "MEDIUM"
        else:
            return "HIGH"
