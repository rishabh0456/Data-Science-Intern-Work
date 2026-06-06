import pandas as pd
import json

# 1. Load Data
df = pd.read_csv('raw_data.csv')

# 2. Clean Data & Handle Missing Values
df['Category'] = df['Category'].fillna('Unknown')
df['Region'] = df['Region'].fillna('Unknown')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['CustomerAge'] = pd.to_numeric(df['CustomerAge'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Impute numerical missing values with median
df['Price'] = df['Price'].fillna(df['Price'].median())
df['CustomerAge'] = df['CustomerAge'].fillna(df['CustomerAge'].median())
df['Quantity'] = df['Quantity'].fillna(df['Quantity'].median())

# Date parsing
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Date'] = df['Date'].fillna(pd.Timestamp('2025-01-01'))
df['Day'] = df['Date'].dt.date.astype(str)

# Calculate derived metrics
df['Revenue'] = df['Price'] * df['Quantity']

# 3. Calculate Summary Statistics
total_transactions = len(df)
total_revenue = df['Revenue'].sum()
avg_price = df['Price'].mean()
avg_age = df['CustomerAge'].mean()

# 4. Aggregate Data for Visualizations
cat_sales = df.groupby('Category')['Revenue'].sum().reset_index(name='Total Sales')
cat_sales_json = cat_sales.to_json(orient='records')

reg_sales = df.groupby('Region')['Revenue'].sum().reset_index(name='Total Sales')
reg_sales_json = reg_sales.to_json(orient='records')

daily_sales = df.groupby('Day')['Revenue'].sum().reset_index(name='Total Sales')
daily_sales_json = daily_sales.to_json(orient='records')

# For scatter plot: Age vs Revenue
scatter_df = df[['CustomerAge', 'Revenue']].dropna().sample(min(1000, len(df)))
scatter_json = scatter_df.to_json(orient='records')

# Correlation matrix
corr_matrix = df[['CustomerAge', 'Quantity', 'Price', 'Revenue']].corr()
corr_json = corr_matrix.to_json()

# 5. Generate HTML Report
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDA Report: Raw Data Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-1: #3b82f6;
            --accent-2: #8b5cf6;
            --accent-3: #ec4899;
            --glass-border: rgba(255, 255, 255, 0.1);
        }}
        body {{
            margin: 0;
            padding: 40px 20px;
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,0.2) 0, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        h1 {{
            font-weight: 800;
            font-size: 3.5rem;
            margin-bottom: 15px;
            background: -webkit-linear-gradient(45deg, var(--accent-1), var(--accent-3));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 1s ease-out;
        }}
        .subtitle {{
            color: var(--text-muted);
            font-size: 1.2rem;
            max-width: 600px;
            margin: 0 auto;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
            margin-bottom: 50px;
        }}
        .kpi-card {{
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }}
        .kpi-card:hover::before {{
            opacity: 1;
        }}
        .kpi-title {{
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
        }}
        .kpi-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        .chart-card {{
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            height: 450px;
        }}
        .chart-card.full-width {{
            grid-column: 1 / -1;
            height: 500px;
        }}
        .chart-title {{
            font-weight: 600;
            font-size: 1.3rem;
            margin-bottom: 25px;
            color: white;
            display: flex;
            align-items: center;
        }}
        .chart-title::before {{
            content: '';
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--accent-2);
            margin-right: 12px;
        }}
        .chart-container {{
            position: relative;
            height: calc(100% - 60px);
            width: 100%;
        }}
        canvas {{
            width: 100% !important;
            height: 100% !important;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Exploratory Data Analysis</h1>
            <div class="subtitle">Uncovering insights, correlations, and trends from our dataset using statistical modeling and premium visualizations.</div>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Total Transactions</div>
                <div class="kpi-value">{total_transactions:,}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">${total_revenue:,.2f}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Average Price</div>
                <div class="kpi-value">${avg_price:,.2f}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Average Age</div>
                <div class="kpi-value">{avg_age:.1f}</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card full-width">
                <div class="chart-title">Revenue Trend Over Time</div>
                <div class="chart-container">
                    <canvas id="timeSeriesChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">Revenue by Category</div>
                <div class="chart-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">Revenue by Region</div>
                <div class="chart-container">
                    <canvas id="regionChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card full-width">
                <div class="chart-title">Customer Age vs. Transaction Revenue</div>
                <div class="chart-container">
                    <canvas id="scatterChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Data injected from Python
        const catData = {cat_sales_json};
        const regData = {reg_sales_json};
        const dailyData = {daily_sales_json};
        const scatterData = {scatter_json};

        // Chart defaults for dark theme
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';
        Chart.defaults.font.family = "'Inter', sans-serif";

        // 1. Revenue by Category (Bar Chart)
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                labels: catData.map(d => d.Category),
                datasets: [{{
                    label: 'Revenue ($)',
                    data: catData.map(d => d['Total Sales']),
                    backgroundColor: 'rgba(59, 130, 246, 0.8)',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    borderRadius: 6,
                    hoverBackgroundColor: '#3b82f6'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});

        // 2. Revenue by Region (Doughnut Chart)
        new Chart(document.getElementById('regionChart'), {{
            type: 'doughnut',
            data: {{
                labels: regData.map(d => d.Region),
                datasets: [{{
                    data: regData.map(d => d['Total Sales']),
                    backgroundColor: [
                        '#3b82f6', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {{
                    legend: {{ position: 'right' }}
                }}
            }}
        }});

        // 3. Time Series Chart (Line Chart with Gradient)
        const ctxTime = document.getElementById('timeSeriesChart').getContext('2d');
        const gradientTime = ctxTime.createLinearGradient(0, 0, 0, 400);
        gradientTime.addColorStop(0, 'rgba(236, 72, 153, 0.5)');
        gradientTime.addColorStop(1, 'rgba(236, 72, 153, 0.0)');

        new Chart(ctxTime, {{
            type: 'line',
            data: {{
                labels: dailyData.map(d => d.Day),
                datasets: [{{
                    label: 'Daily Revenue ($)',
                    data: dailyData.map(d => d['Total Sales']),
                    borderColor: '#ec4899',
                    backgroundColor: gradientTime,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    intersect: false,
                    mode: 'index',
                }},
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});

        // 4. Scatter Chart (Age vs Revenue)
        new Chart(document.getElementById('scatterChart'), {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'Transactions',
                    data: scatterData.map(d => ({{ x: d.CustomerAge, y: d.Revenue }})),
                    backgroundColor: 'rgba(16, 185, 129, 0.6)',
                    borderColor: '#10b981',
                    borderWidth: 1,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }}]
            }},
            options: {{ 
                responsive: true, 
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Customer Age' }} }},
                    y: {{ title: {{ display: true, text: 'Revenue ($)' }} }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('eda_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("EDA Report generated successfully at eda_report.html")
