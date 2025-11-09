import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from model.transformer_model import ThreatDetectionTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns

def generate_synthetic_data(num_samples=1000):
    """Generate synthetic training data"""
    X = []
    y = []
    
    for _ in range(num_samples):
        # Generate features
        url_length = np.random.uniform(0, 1)
        has_ip = np.random.choice([0, 1], p=[0.9, 0.1])
        has_suspicious = np.random.choice([0, 1], p=[0.7, 0.3])
        subdomains = np.random.uniform(0, 1)
        has_https = np.random.choice([0, 1], p=[0.3, 0.7])
        domain_age = np.random.uniform(0, 1)
        special_chars = np.random.uniform(0, 1)
        has_redirect = np.random.choice([0, 1], p=[0.8, 0.2])
        
        features = [url_length, has_ip, has_suspicious, subdomains, 
                   has_https, domain_age, special_chars, has_redirect]
        
        # Generate label (1 = threat, 0 = safe)
        threat_indicators = has_ip + has_suspicious + (1 - has_https) + has_redirect
        is_threat = 1 if threat_indicators >= 2 else 0
        
        X.append(features)
        y.append(is_threat)
    
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

def train_model(epochs=50):
    model = ThreatDetectionTransformer()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    X, y = generate_synthetic_data(2000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = torch.FloatTensor(X_train)
    y_train = torch.FloatTensor(y_train).unsqueeze(1)
    X_test = torch.FloatTensor(X_test)
    y_test = torch.FloatTensor(y_test).unsqueeze(1)
    
    print("Training Transformer model...")
    model.train()
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            accuracy = ((outputs > 0.5).float() == y_train).float().mean()
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy.item():.4f}')
    
    torch.save(model.state_dict(), 'pretrained/model_weights.pth')
    print("Model saved successfully!")
    
    evaluate_and_visualize(model, X_test, y_test)
    
    return model

def evaluate_and_visualize(model, X_test, y_test):
    """Evaluate the model and generate visualizations."""
    model.eval()
    with torch.no_grad():
        outputs = model(X_test)
        y_pred = (outputs > 0.5).float()

    y_test_np = y_test.numpy()
    y_pred_np = y_pred.numpy()

    # Metrics
    accuracy = accuracy_score(y_test_np, y_pred_np)
    precision = precision_score(y_test_np, y_pred_np)
    recall = recall_score(y_test_np, y_pred_np)
    f1 = f1_score(y_test_np, y_pred_np)

    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1-score: {f1:.4f}')

    # Confusion Matrix
    cm = confusion_matrix(y_test_np, y_pred_np)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig('confusion_matrix.png')
    plt.show()

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test_np, outputs.numpy())
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc='lower right')
    plt.savefig('roc_curve.png')
    plt.show()

    # Precision-Recall Curve
    precision, recall, _ = precision_recall_curve(y_test_np, outputs.numpy())
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.savefig('precision_recall_curve.png')
    plt.show()

    # Metrics Bar Chart
    metrics = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1-score': f1}
    plt.figure(figsize=(8, 6))
    sns.barplot(x=list(metrics.keys()), y=list(metrics.values()))
    plt.title('Performance Metrics')
    plt.ylabel('Score')
    plt.ylim(0, 1)
    plt.savefig('metrics_bar_chart.png')
    plt.show()

    # Histogram of Prediction Probabilities
    plt.figure(figsize=(8, 6))
    plt.hist(outputs.numpy().flatten(), bins=20, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Histogram of Prediction Probabilities')
    plt.xlabel('Predicted Probability')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig('prediction_probabilities_histogram.png')
    plt.show()

if __name__ == '__main__':
    import os
    os.makedirs('pretrained', exist_ok=True)
    train_model()
