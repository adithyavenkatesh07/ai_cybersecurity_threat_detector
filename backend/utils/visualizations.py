import torch
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, accuracy_score, precision_score, recall_score, f1_score
from model.transformer_model import ThreatDetectionTransformer
from model.train_model import generate_synthetic_data

def get_model_metrics():
    """
    Generates model evaluation metrics and data for visualizations.
    """
    # Load model and data
    model = ThreatDetectionTransformer()
    # model.load_state_dict(torch.load('model/pretrained/model_weights.pth')) # This will be needed later
    model.eval()

    X, y = generate_synthetic_data(1000)
    X_tensor = torch.FloatTensor(X)
    y_tensor = torch.FloatTensor(y).unsqueeze(1)

    with torch.no_grad():
        outputs = model(X_tensor)
        y_pred = (outputs > 0.5).float()

    y_true_np = y_tensor.numpy()
    y_pred_np = y_pred.numpy()
    y_scores_np = outputs.numpy()

    # --- Scalar Metrics ---
    metrics = {
        "accuracy": accuracy_score(y_true_np, y_pred_np),
        "precision": precision_score(y_true_np, y_pred_np),
        "recall": recall_score(y_true_np, y_pred_np),
        "f1_score": f1_score(y_true_np, y_pred_np)
    }

    # --- Confusion Matrix ---
    cm = confusion_matrix(y_true_np, y_pred_np)
    confusion_matrix_data = {
        "labels": ["Safe", "Threat"],
        "values": cm.tolist()
    }

    # --- ROC Curve ---
    fpr, tpr, _ = roc_curve(y_true_np, y_scores_np)
    roc_data = {
        "fpr": fpr.tolist(),
        "tpr": tpr.tolist()
    }

    # --- Precision-Recall Curve ---
    precision, recall, _ = precision_recall_curve(y_true_np, y_scores_np)
    pr_curve_data = {
        "precision": precision.tolist(),
        "recall": recall.tolist()
    }

    return {
        "metrics": metrics,
        "confusion_matrix": confusion_matrix_data,
        "roc_curve": roc_data,
        "precision_recall_curve": pr_curve_data
    }

def generate_visualization_data(analysis_data):
    """
    Formats the raw analysis data into a structure suitable for frontend charts.
    """
    if 'error' in analysis_data:
        return {'error': analysis_data['error']}
        
    # SEO Structure (Donut Chart)
    seo_headings = analysis_data.get('seo_metrics', {}).get('heading_counts', {})
    seo_chart_data = {
        'labels': list(seo_headings.keys()),
        'values': list(seo_headings.values())
    }
    
    # Link Analysis (Bar Chart)
    link_data = {
        'internal': analysis_data.get('seo_metrics', {}).get('internal_links', 0),
        'external': analysis_data.get('seo_metrics', {}).get('external_links', 0)
    }
    
    # Page Asset Size (Pie Chart) - Simplified
    asset_sizes = analysis_data.get('performance_metrics', {}).get('asset_size_distribution_kb', {})
    asset_chart_data = {
        'labels': list(asset_sizes.keys()),
        'values': list(asset_sizes.values())
    }
    
    # Keyword Density (Horizontal Bar Chart)
    keyword_data = analysis_data.get('seo_metrics', {}).get('keyword_density', [])
    keyword_chart_data = {
        'keywords': [item['keyword'] for item in keyword_data],
        'counts': [item['count'] for item in keyword_data]
    }
    
    return {
        'seo_heading_chart': seo_chart_data,
        'link_analysis_chart': link_data,
        'asset_size_chart': asset_chart_data,
        'keyword_density_chart': keyword_chart_data
    }