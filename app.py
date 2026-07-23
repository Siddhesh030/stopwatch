import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load the pickle model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'dtmodel.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model file: {e}")
    model = None

# High-end Animated, Dual-Theme UI with Integrated Visualizations
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predictive Analytics Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            /* Dark Theme Variables */
            --bg-grad: linear-gradient(135deg, #09090b 0%, #16161a 100%);
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --text-main: #f4f4f5;
            --text-muted: #a1a1aa;
            --input-bg: rgba(24, 24, 27, 0.6);
            --accent-glow: linear-gradient(135deg, #6366f1, #a855f7);
            --shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
        }

        [data-theme="light"] {
            /* Light Theme Variables */
            --bg-grad: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            --glass-bg: rgba(255, 255, 255, 0.45);
            --glass-border: rgba(15, 23, 42, 0.08);
            --text-main: #0f172a;
            --text-muted: #64748b;
            --input-bg: rgba(255, 255, 255, 0.7);
            --accent-glow: linear-gradient(135deg, #4f46e5, #7c3aed);
            --shadow: 0 30px 60px rgba(15, 23, 42, 0.08);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: background 0.4s ease, border 0.4s ease;
        }

        body {
            background: var(--bg-grad);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: var(--text-main);
            overflow-x: hidden;
            padding: 40px 20px;
            position: relative;
        }

        /* Ambient Dynamic Background Glows */
        .ambient-orb {
            position: absolute;
            background: var(--accent-glow);
            border-radius: 50%;
            filter: blur(120px);
            z-index: 0;
            opacity: 0.4;
            animation: pulse 8s ease-in-out infinite alternate;
        }
        .orb-1 { width: 400px; height: 400px; top: -5%; left: 10%; }
        .orb-2 { width: 450px; height: 450px; bottom: -5%; right: 10%; animation-delay: -4s; }

        @keyframes pulse {
            0% { transform: translate(0, 0) scale(1); opacity: 0.3; }
            100% { transform: translate(20px, -40px) scale(1.15); opacity: 0.5; }
        }

        /* Theme Switcher Layout */
        .theme-toggle-container {
            position: absolute;
            top: 25px;
            right: 25px;
            z-index: 100;
        }

        .theme-btn {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            padding: 10px 18px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Dashboard Grid Interface */
        .dashboard-layout {
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            width: 100%;
            max-width: 1100px;
            position: relative;
            z-index: 10;
        }

        @media (min-width: 850px) {
            .dashboard-layout {
                grid-template-columns: 1.1fr 0.9fr;
            }
        }

        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--glass-border);
            border-radius: 28px;
            padding: 35px;
            box-shadow: var(--shadow);
            animation: slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }

        .gradient-text {
            background: var(--accent-glow);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 25px;
        }

        /* Form Configuration */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 18px;
        }
        @media (min-width: 480px) {
            .form-grid { grid-template-columns: 1fr 1fr; }
            .full-width { grid-column: span 2; }
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-main);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            opacity: 0.8;
        }

        input, select {
            width: 100%;
            padding: 14px 18px;
            background: var(--input-bg);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            color: var(--text-main);
            font-size: 0.95rem;
            font-weight: 500;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.25);
        }

        button.submit-btn {
            width: 100%;
            padding: 16px;
            background: var(--accent-glow);
            border: none;
            border-radius: 14px;
            color: white;
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.35);
            transition: all 0.3s ease;
        }

        button.submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.5);
        }

        /* Visualization & Result Side */
        .visualization-side {
            display: flex;
            flex-direction: column;
            gap: 25px;
            justify-content: space-between;
        }

        .chart-container {
            flex-grow: 1;
            min-height: 260px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        /* Interactive Result Display */
        .result-box {
            padding: 24px;
            border-radius: 18px;
            text-align: center;
            font-weight: 700;
            font-size: 1.1rem;
            display: none;
            backdrop-filter: blur(10px);
            animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        @keyframes popIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }

        .res-yes {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #10b981;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.1);
        }

        .res-no {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #ef4444;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.1);
        }
    </style>
</head>
<body>

    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>

    <div class="theme-toggle-container">
        <button class="theme-btn" id="themeToggleBtn">
            <span id="themeIcon">☀️</span> <span id="themeText">Light Mode</span>
        </button>
    </div>

    <div class="dashboard-layout">
        <!-- Input Form Section -->
        <div class="glass-card">
            <h2>Decision Tree <span class="gradient-text">Engine</span></h2>
            <p class="subtitle">Update metrics to trigger serverless calculations instantly.</p>
            
            <form id="analyticsForm">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="age">Age Metric</label>
                        <input type="number" id="age" name="Age" required min="1" max="120" value="28">
                    </div>

                    <div class="form-group">
                        <label for="gender">Gender Configuration</label>
                        <select id="gender" name="Gender" required>
                            <option value="1" selected>Male</option>
                            <option value="0">Female</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="region">Region Code</label>
                        <input type="number" id="region" name="Region" required value="2">
                    </div>

                    <div class="form-group">
                        <label for="occupation">Occupation Index</label>
                        <input type="number" id="occupation" name="Occupation" required value="4">
                    </div>

                    <div class="form-group full-width">
                        <label for="income">Normalized Income</label>
                        <input type="number" id="income" name="Income" required value="45000">
                    </div>
                    
                    <div class="form-group full-width" style="margin-top: 10px;">
                        <button type="submit" class="submit-btn">Run Engine Assessment</button>
                    </div>
                </div>
            </form>
        </div>

        <!-- Metrics Chart Visualization & Results Card -->
        <div class="glass-card visualization-side">
            <div>
                <h3 style="font-family:'Space Grotesk'; font-size:1.3rem; margin-bottom:5px;">Input Profile Breakdown</h3>
                <p class="subtitle" style="margin-bottom:15px;">Proportional metrics structure for the current execution run</p>
            </div>
            
            <div class="chart-container">
                <canvas id="metricsChart"></canvas>
            </div>

            <div id="predictionOutput" class="result-box"></div>
        </div>
    </div>

    <script>
        // Theme Toggle Manager
        const themeBtn = document.getElementById('themeToggleBtn');
        const themeIcon = document.getElementById('themeIcon');
        const themeText = document.getElementById('themeText');
        const htmlEl = document.documentElement;

        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlEl.getAttribute('data-theme');
            if(currentTheme === 'dark') {
                htmlEl.setAttribute('data-theme', 'light');
                themeIcon.innerText = '🌙';
                themeText.innerText = 'Dark Mode';
            } else {
                htmlEl.setAttribute('data-theme', 'dark');
                themeIcon.innerText = '☀️';
                themeText.innerText = 'Light Mode';
            }
            if(window.myChart) { updateChartTheme(); }
        });

        // Interactive Visuals Implementation (Chart.js Configuration)
        const ctx = document.getElementById('metricsChart').getContext('2d');
        window.myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Age', 'Gender', 'Region', 'Occupation', 'Income Scaling'],
                datasets: [{
                    data: [28, 1, 2, 4, 45], 
                    backgroundColor: [
                        '#6366f1',
                        '#a855f7',
                        '#f43f5e',
                        '#10b981',
                        '#f59e0b'
                    ],
                    borderWidth: 0,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#a1a1aa',
                            font: { family: 'Plus Jakarta Sans', weight: '600', size: 11 },
                            padding: 15
                        }
                    }
                },
                cutout: '70%'
            }
        });

        function updateChartTheme() {
            const isLight = htmlEl.getAttribute('data-theme') === 'light';
            window.myChart.options.plugins.legend.labels.color = isLight ? '#64748b' : '#a1a1aa';
            window.myChart.update();
        }

        // Live API Submission handling
        document.getElementById('analyticsForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const ageVal = parseFloat(formData.get('Age'));
            const genderVal = parseFloat(formData.get('Gender'));
            const regionVal = parseFloat(formData.get('Region'));
            const occVal = parseFloat(formData.get('Occupation'));
            const incomeVal = parseFloat(formData.get('Income'));

            // Dynamically refresh the Pie Chart view mapping data structures 
            window.myChart.data.datasets[0].data = [
                ageVal, 
                genderVal * 10, 
                regionVal * 10, 
                occVal * 10, 
                incomeVal / 1000
            ];
            window.myChart.update();

            const outputDiv = document.getElementById('predictionOutput');
            outputDiv.style.display = 'none';

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        Age: ageVal,
                        Gender: genderVal,
                        Region: regionVal,
                        Occupation: occVal,
                        Income: incomeVal
                    })
                });
                
                const resData = await response.json();
                
                if (resData.prediction) {
                    const cleanPrediction = resData.prediction.toLowerCase().replace(/['"\[\]]/g, '').trim();
                    outputDiv.innerText = `System Status Result: ${cleanPrediction.toUpperCase()}`;
                    outputDiv.className = `result-box ${cleanPrediction === 'yes' ? 'res-yes' : 'res-no'}`;
                    outputDiv.style.display = 'block';
                } else {
                    outputDiv.innerText = "Error tracking prediction structure.";
                    outputDiv.className = 'result-box res-no';
                    outputDiv.style.display = 'block';
                }
            } catch (err) {
                outputDiv.innerText = "Target infrastructure communication error.";
                outputDiv.className = 'result-box res-no';
                outputDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Order inputs strictly matching: Age, Gender, Region, Occupation, Income
        features = [
            float(data['Age']),
            float(data['Gender']),
            float(data['Region']),
            float(data['Occupation']),
            float(data['Income'])
        ]
        
        # Log array structure to local terminal for precise dataset testing
        print(f"--- Processing Input Features Vector: {features} ---")
        
        # Reshape for single sample execution
        final_features = np.array([features])
        
        if model is not None:
            raw_prediction = model.predict(final_features)
            # Standardize string formatting from numpy output types
            prediction_val = str(raw_prediction[0]).strip().lower()
        else:
            # Fallback mock setup if pkl is missing or corrupt during testing
            prediction_val = 'no'
        
        return jsonify({'prediction': prediction_val})
        
    except Exception as e:
        print(f"Prediction Error Trace: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
