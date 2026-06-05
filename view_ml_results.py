import pandas as pd
import webbrowser
import os
import base64

df = pd.read_csv('ml_dataset.csv')
html_table = df.head(100).to_html(classes='table table-striped table-hover', index=False)

with open('reports/model_metrics.txt', 'r') as f:
    metrics = f.read().replace('\n', '<br>')

def get_base64_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

img1_b64 = get_base64_image('reports/6_confusion_matrices.png')
img2_b64 = get_base64_image('reports/7_roc_curve.png')

html_content = f'''<!DOCTYPE html>
<html>
<head>
<title>Machine Learning Results Dashboard</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body {{ background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    .container {{ max-width: 95%; margin-top: 2rem; }}
    .card {{ border: none; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .card-header {{ background-color: #343a40; color: white; border-radius: 12px 12px 0 0 !important; font-weight: bold; }}
    .img-fluid {{ border-radius: 8px; }}
    .table-container {{ max-height: 400px; overflow-y: auto; }}
    th {{ position: sticky; top: 0; background-color: #343a40 !important; color: white !important; }}
</style>
</head>
<body>
    <div class="container mb-5">
        <h1 class="mb-4 text-center">Machine Learning Predictive Modeling Dashboard</h1>
        
        <div class="row">
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-header text-center">Model Accuracy Metrics</div>
                    <div class="card-body d-flex align-items-center justify-content-center">
                        <h4 class="text-center text-primary" style="line-height: 1.8;">
                            {metrics}
                        </h4>
                    </div>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Generated ML Dataset Sample (First 100 rows)</div>
                    <div class="card-body p-0">
                        <div class="table-container p-3">
                            {html_table}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header text-center">Confusion Matrices</div>
                    <div class="card-body text-center">
                        <img src="data:image/png;base64,{img1_b64}" class="img-fluid" alt="Confusion Matrices">
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header text-center">ROC Curve Analysis</div>
                    <div class="card-body text-center">
                        <img src="data:image/png;base64,{img2_b64}" class="img-fluid" alt="ROC Curve">
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

file_path = os.path.abspath('ml_dashboard.html')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

webbrowser.open('file://' + file_path)
