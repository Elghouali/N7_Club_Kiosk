#!/usr/bin/env python
"""
Export static HTML for GitHub Pages deployment.
Renders the Flask template with live data from Google Sheets and writes it to docs/index.html.
Works in GitHub Actions with secrets.
"""

import os
from dotenv import load_dotenv
from app import app, generate_qr_base64

# Load environment variables
load_dotenv()

# Configuration
AWS_LINK = "https://chat.whatsapp.com/DzEjjfEHm8E5FqU5ADNrJh"
OUTPUT_DIR = "docs"

def export_static_html():
    """Render and export the index.html template to docs/index.html"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Try to get live member count from Google Sheets (optional)
    count = 0
    try:
        from google_sheets_client import get_member_count
        count = get_member_count()
        print(f"✓ Exported with live count: {count} members")
    except Exception as e:
        print(f"Note: Using default count (0). Google Sheets access: {e}")
    
    qr_code_data = generate_qr_base64(AWS_LINK)
    
    # Use Flask's test request context to render templates
    with app.test_request_context('/'):
        from flask import render_template
        rendered_html = render_template('index.html', count=count, qr_code=qr_code_data)
    
    # Write to docs/index.html
    output_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    
    print(f"✓ Static HTML exported to {output_path}")

if __name__ == '__main__':
    export_static_html()
