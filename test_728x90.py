#!/usr/bin/env python3
"""Test script per generare 728x90 con template attuale"""

from template_engine import TemplateEngine, load_template
import base64

# Inizializza engine
engine = TemplateEngine()
engine.load_fonts()

# Carica template 728x90
template = load_template('templates/728x90.json')

# Carica logo small (su sfondo scuro - bianco)
with open('images/G_bianco.png', 'rb') as f:
    logo_data = base64.b64encode(f.read()).decode('utf-8')

# Imposta dati di test (come Bologna)
engine.set_content_data({
    'header_text': 'PROMO FLASH',
    'main_title': 'IMPRESA BOLOGNA',
    'subtitle': '',
    'cta_text': 'ABBONATI',
    'price': '14,99€',
    'price_period': '/ANNO',
    'price_full': '14,99€\n/ANNO',
    'logo_small_dark': f'data:image/png;base64,{logo_data}'
})

# Carica background
with open('background/bg15.png', 'rb') as f:
    bg_data = base64.b64encode(f.read()).decode('utf-8')

engine.set_background({
    'image_data': bg_data,
    'color': '#8B0000'  # Bordeaux fallback
})

# Renderizza
svg = engine.render_template(template)

# Salva
with open('output/test_728x90_current.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print('✅ Generato: output/test_728x90_current.svg')
print(f'   Dimensioni: {template["width"]}x{template["height"]}')
