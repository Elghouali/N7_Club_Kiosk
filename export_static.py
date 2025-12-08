#!/usr/bin/env python
"""
Export static HTML for GitHub Pages deployment.
Renders the Flask template with sample data and writes it to docs/index.html
"""

import os
from app import app, generate_qr_base64

# Configuration
AWS_LINK = "https://chat.whatsapp.com/DzEjjfEHm8E5FqU5ADNrJh"
OUTPUT_DIR = "docs"

def export_static_html():
    """Render and export the index.html template to docs/index.html"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Sample data for static export
    count = 0  # Default member count (will be updated when Flask runs)
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
