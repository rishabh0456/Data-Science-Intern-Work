import pandas as pd
import webbrowser
import os

df = pd.read_csv('cleaned_data.csv')

html_table = df.to_html(classes='table table-striped table-hover', index=False)

html_content = f'''<!DOCTYPE html>
<html>
<head>
<title>Data Visualization Table</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body {{ background-color: #f8f9fa; }}
    .container {{ max-width: 95%; margin-top: 2rem; }}
    .table-container {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        max-height: 80vh;
        overflow-y: auto;
    }}
    th {{ position: sticky; top: 0; background-color: #343a40 !important; color: white !important; }}
</style>
</head>
<body>
    <div class="container">
        <h2 class="mb-4 text-center">Cleaned Dataset Explorer</h2>
        <div class="table-container">
            {html_table}
        </div>
    </div>
</body>
</html>'''

file_path = os.path.abspath('interactive_table.html')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

webbrowser.open('file://' + file_path)
