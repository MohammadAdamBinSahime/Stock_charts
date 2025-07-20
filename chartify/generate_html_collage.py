import os
import glob
from datetime import datetime

def generate_html_collage():
    """Generate HTML collage of all stock charts"""
    
    # Find all PNG files in stock_png directory (excluding archive)
    png_files = [f for f in glob.glob("stock_png/*.png") if not f.startswith("stock_png/archive")]
    
    if not png_files:
        print("No PNG files found in stock_png/ directory")
        return
    
    print(f"Found {len(png_files)} PNG files to include in collage")
    
    # Sort files for consistent ordering
    png_files.sort()
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, maximum-scale=5.0, minimum-scale=0.5">
    <title>Stock Charts Collage</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 10px;
            margin: 0 auto;
        }}
        .chart-container {{
            background: white;
            border-radius: 4px;
            padding: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .chart-title {{
            font-size: 10px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }}
        .chart-image {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        .stats {{
            text-align: center;
            margin-bottom: 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Stock Charts Collage</h1>
        <div class="stats">
            Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            Total Charts: {len(png_files)}
        </div>
    </div>
    
    <div class="charts-grid">
"""
    
    # Add each chart to the grid
    for png_file in png_files:
        # Extract filename without path and extension for title
        chart_name = os.path.basename(png_file).rsplit('.', 1)[0]
        
        html_content += f"""        <div class="chart-container">
            <div class="chart-title">{chart_name}</div>
            <img src="{png_file}" alt="{chart_name}" class="chart-image">
        </div>
"""
    
    # Close HTML
    html_content += """    </div>
</body>
</html>"""
    
    # Write HTML file
    output_file = "stock_charts_collage.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML collage generated: {output_file}")
    print(f"Open {output_file} in your browser to view the collage")

def main():
    """Main function"""
    generate_html_collage()

if __name__ == "__main__":
    main()