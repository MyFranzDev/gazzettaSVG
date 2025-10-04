#!/usr/bin/env python3
"""
Single banner generator - Called by PHP frontend
Receives JSON data and generates one SVG banner
"""

import sys
import json
import base64
import warnings

# Suppress all warnings to avoid polluting SVG output
warnings.filterwarnings('ignore')

from template_engine import TemplateEngine, load_template

def generate_banner(data_json):
    """Generate a single banner from JSON data"""

    # Parse input data
    data = json.loads(data_json)

    # Initialize engine
    engine = TemplateEngine()
    engine.load_fonts()

    # Load template
    template_file = f"templates/{data['template']}.json"
    template = load_template(template_file)

    # Set content data
    engine.set_content_data({
        'header_text': data.get('header_text', ''),
        'main_title': data.get('main_title', ''),
        'description_text': data.get('description_text', ''),
        'cta_text': data.get('cta_text', ''),
        'price': data.get('price', ''),
        'price_period': data.get('price_period', ''),
        'header_title_combined': f"{data.get('header_text', '')} | {data.get('main_title', '')}",
        # Logos will be added from uploaded files
        'logo_small_dark': data.get('logo_small_dark'),
        'logo_large_dark': data.get('logo_large_dark'),
        'user_image': data.get('user_image')
    })

    # Set background
    bg_id = data.get('background', 'bg01')
    try:
        with open(f'web/frontend/backgrounds/{bg_id}.png', 'rb') as f:
            bg_data = base64.b64encode(f.read()).decode('utf-8')
    except FileNotFoundError:
        bg_data = None

    engine.set_background({
        'image_data': bg_data,
        'color': '#0f364c'  # Fallback color
    })

    # Render template
    svg = engine.render_template(template)

    # Output SVG to stdout
    print(svg)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No data provided", file=sys.stderr)
        sys.exit(1)

    generate_banner(sys.argv[1])
