import React from 'react';
import { Bar, Line } from 'react-chartjs-2';
import Visualizations from './Visualizations';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MetricsReport = ({ metricsData, visualizationsData }) => {
  if (!metricsData) {
    return null;
  }

  const { metrics, confusion_matrix, roc_curve, precision_recall_curve } = metricsData;

  const metricsChartData = {
    labels: Object.keys(metrics),
    datasets: [
      {
        label: 'Model Performance',
        data: Object.values(metrics),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const rocCurveData = {
    labels: roc_curve.fpr,
    datasets: [
      {
        label: 'ROC Curve',
        data: roc_curve.tpr,
        fill: false,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
    ],
  };

  const prCurveData = {
    labels: precision_recall_curve.recall,
    datasets: [
      {
        label: 'Precision-Recall Curve',
        data: precision_recall_curve.precision,
        fill: false,
        borderColor: 'rgb(54, 162, 235)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="metrics-report">
      <h3>Model Performance Metrics</h3>
      <div className="charts-grid">
        <div className="chart-container">
          <h4>Performance Metrics</h4>
          <Bar data={metricsChartData} />
        </div>
        <div className="chart-container">
          <h4>ROC Curve</h4>
          <Line data={rocCurveData} />
        </div>
        <div className="chart-container">
          <h4>Precision-Recall Curve</h4>
          <Line data={prCurveData} />
        </div>
        <div className="chart-container">
          <h4>Confusion Matrix</h4>
          <div className="confusion-matrix">
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th>Predicted Safe</th>
                  <th>Predicted Threat</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Actual Safe</th>
                  <td>{confusion_matrix.values[0][0]}</td>
                  <td>{confusion_matrix.values[0][1]}</td>
                </tr>
                <tr>
                  <th>Actual Threat</th>
                  <td>{confusion_matrix.values[1][0]}</td>
                  <td>{confusion_matrix.values[1][1]}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      {visualizationsData && <Visualizations data={visualizationsData} />}
    </div>
  );
};

export default MetricsReport;
