import React from 'react';
import { Doughnut, Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const Visualizations = ({ data }) => {
    if (!data) {
        return <p>No visualization data available.</p>;
    }

    // 1. SEO Structure Breakdown (Donut Chart)
    const seoChartData = {
        labels: data.seo_heading_chart?.labels || [],
        datasets: [
            {
                label: 'Heading Tags',
                data: data.seo_heading_chart?.values || [],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ],
                hoverBackgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ]
            }
        ]
    };

    // 2. Link Analysis (Stacked Bar Chart)
    const linkChartData = {
        labels: ['Links'],
        datasets: [
            {
                label: 'Internal Links',
                data: [data.link_analysis_chart?.internal || 0],
                backgroundColor: '#36A2EB',
            },
            {
                label: 'External Links',
                data: [data.link_analysis_chart?.external || 0],
                backgroundColor: '#FF6384',
            }
        ]
    };

    const linkChartOptions = {
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true
            }
        }
    };

    // 3. Page Asset Size (Pie Chart)
    const assetSizeChartData = {
        labels: data.asset_size_chart?.labels || [],
        datasets: [{
            data: data.asset_size_chart?.values || [],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
        }],
    };

    // 4. Keyword Density (Horizontal Bar Chart)
    const keywordDensityChartData = {
        labels: data.keyword_density_chart?.keywords || [],
        datasets: [{
            label: 'Keyword Count',
            data: data.keyword_density_chart?.counts || [],
            backgroundColor: '#9966FF',
        }],
    };

    return (
        <div className="visualizations-container">
            <h2>Scan Visualizations</h2>
            <div className="chart-row">
                <div className="chart-container">
                    <h3>SEO Heading Structure</h3>
                    <Doughnut data={seoChartData} />
                </div>
                <div className="chart-container">
                    <h3>Link Analysis</h3>
                    <Bar data={linkChartData} options={linkChartOptions} />
                </div>
            </div>
            <div className="chart-row">
                <div className="chart-container">
                    <h3>Page Asset Size (KB)</h3>
                    <Pie data={assetSizeChartData} />
                </div>
                <div className="chart-container">
                    <h3>Top Keywords</h3>
                    <Bar data={keywordDensityChartData} options={{ indexAxis: 'y' }} />
                </div>
            </div>
        </div>
    );
};

export default Visualizations;