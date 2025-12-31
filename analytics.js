// Project: Surveillance Video Dataset
// Author: Molla Samser
// Website: https://rskworld.in/
// Contact: help@rskworld.in
// Phone: +91 93305 39277
// Address: Nutanhat, Mongolkote, Purba Burdwan, West Bengal, India, 713147

// Analytics Dashboard JavaScript

let detectionsChart, anomalyChart, activityChart, processingChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadAnalyticsData();
    initializeCharts();
    startRealTimeUpdates();
});

function loadAnalyticsData() {
    // Load data from API or local files
    fetch('api/analytics')
        .then(response => response.json())
        .then(data => {
            updateStatistics(data);
            updateCharts(data);
            updateTimeline(data.events);
        })
        .catch(() => {
            // Fallback to sample data
            const sampleData = getSampleAnalyticsData();
            updateStatistics(sampleData);
            updateCharts(sampleData);
            updateTimeline(sampleData.events);
        });
}

function getSampleAnalyticsData() {
    return {
        totalVideos: 2,
        totalDetections: 156,
        totalAnomalies: 2,
        totalHours: 0.5,
        detections: [45, 52, 38, 21],
        anomalies: { 'unusual_movement': 2, 'rapid_change': 0 },
        activities: { 'walking': 45, 'standing': 38, 'running': 12 },
        events: [
            { time: '10:30:15', type: 'detection', message: 'Person detected in frame', video: 'sample.mp4' },
            { time: '10:30:45', type: 'anomaly', message: 'Anomaly detected - rapid movement', video: 'sample2.mp4' },
            { time: '10:31:20', type: 'detection', message: 'Multiple persons detected', video: 'sample2.mp4' }
        ]
    };
}

function updateStatistics(data) {
    document.getElementById('totalVideos').textContent = data.totalVideos || 0;
    document.getElementById('totalDetections').textContent = data.totalDetections || 0;
    document.getElementById('totalAnomalies').textContent = data.totalAnomalies || 0;
    document.getElementById('totalHours').textContent = data.totalHours || 0;
}

function initializeCharts() {
    // Detections Chart
    const detectionsCtx = document.getElementById('detectionsChart').getContext('2d');
    detectionsChart = new Chart(detectionsCtx, {
        type: 'line',
        data: {
            labels: ['00:00', '00:05', '00:10', '00:15'],
            datasets: [{
                label: 'Person Detections',
                data: [45, 52, 38, 21],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });

    // Anomaly Chart
    const anomalyCtx = document.getElementById('anomalyChart').getContext('2d');
    anomalyChart = new Chart(anomalyCtx, {
        type: 'doughnut',
        data: {
            labels: ['Unusual Movement', 'Rapid Change', 'Normal'],
            datasets: [{
                data: [2, 0, 154],
                backgroundColor: ['#dc3545', '#ffc107', '#28a745']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });

    // Activity Chart
    const activityCtx = document.getElementById('activityChart').getContext('2d');
    activityChart = new Chart(activityCtx, {
        type: 'bar',
        data: {
            labels: ['Walking', 'Standing', 'Running', 'Other'],
            datasets: [{
                label: 'Activities',
                data: [45, 38, 12, 8],
                backgroundColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });

    // Processing Chart
    const processingCtx = document.getElementById('processingChart').getContext('2d');
    processingChart = new Chart(processingCtx, {
        type: 'bar',
        data: {
            labels: ['Processed', 'Pending', 'Failed'],
            datasets: [{
                label: 'Videos',
                data: [2, 0, 0],
                backgroundColor: ['#28a745', '#ffc107', '#dc3545']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

function updateCharts(data) {
    if (detectionsChart && data.detections) {
        detectionsChart.data.datasets[0].data = data.detections;
        detectionsChart.update();
    }
    
    if (anomalyChart && data.anomalies) {
        const values = Object.values(data.anomalies);
        anomalyChart.data.datasets[0].data = [...values, data.totalDetections - values.reduce((a, b) => a + b, 0)];
        anomalyChart.update();
    }
    
    if (activityChart && data.activities) {
        activityChart.data.datasets[0].data = Object.values(data.activities);
        activityChart.update();
    }
}

function updateTimeline(events) {
    const timeline = document.getElementById('eventsTimeline');
    timeline.innerHTML = '';
    
    if (!events || events.length === 0) {
        timeline.innerHTML = '<p>No recent events</p>';
        return;
    }
    
    events.forEach(event => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        const icon = event.type === 'anomaly' ? 'fa-exclamation-triangle' : 'fa-user';
        const color = event.type === 'anomaly' ? '#dc3545' : '#667eea';
        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <i class="fas ${icon}" style="color: ${color}; margin-right: 10px;"></i>
                    <strong>${event.message}</strong>
                    <span style="color: #666; margin-left: 10px;">${event.video}</span>
                </div>
                <span style="color: #666;">${event.time}</span>
            </div>
        `;
        timeline.appendChild(item);
    });
}

function applyFilters() {
    const dateFilter = document.getElementById('dateFilter').value;
    const videoFilter = document.getElementById('videoFilter').value;
    const anomalyFilter = document.getElementById('anomalyFilter').value;
    
    // Apply filters and reload data
    loadAnalyticsData();
    console.log('Filters applied:', { dateFilter, videoFilter, anomalyFilter });
}

function exportData(format) {
    const data = getSampleAnalyticsData();
    
    switch(format) {
        case 'json':
            downloadJSON(data, 'analytics_data.json');
            break;
        case 'csv':
            downloadCSV(data, 'analytics_data.csv');
            break;
        case 'pdf':
            window.print();
            break;
    }
}

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

function downloadCSV(data, filename) {
    let csv = 'Metric,Value\n';
    csv += `Total Videos,${data.totalVideos}\n`;
    csv += `Total Detections,${data.totalDetections}\n`;
    csv += `Total Anomalies,${data.totalAnomalies}\n`;
    csv += `Total Hours,${data.totalHours}\n`;
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

function startRealTimeUpdates() {
    // Simulate real-time updates every 5 seconds
    setInterval(() => {
        // In production, this would fetch from API
        const newEvent = {
            time: new Date().toLocaleTimeString(),
            type: Math.random() > 0.8 ? 'anomaly' : 'detection',
            message: 'New event detected',
            video: 'sample.mp4'
        };
        
        // Add to timeline
        const timeline = document.getElementById('eventsTimeline');
        const item = document.createElement('div');
        item.className = 'timeline-item';
        const icon = newEvent.type === 'anomaly' ? 'fa-exclamation-triangle' : 'fa-user';
        const color = newEvent.type === 'anomaly' ? '#dc3545' : '#667eea';
        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <i class="fas ${icon}" style="color: ${color}; margin-right: 10px;"></i>
                    <strong>${newEvent.message}</strong>
                    <span style="color: #666; margin-left: 10px;">${newEvent.video}</span>
                </div>
                <span style="color: #666;">${newEvent.time}</span>
            </div>
        `;
        timeline.insertBefore(item, timeline.firstChild);
        
        // Keep only last 10 events
        while (timeline.children.length > 10) {
            timeline.removeChild(timeline.lastChild);
        }
    }, 5000);
}

