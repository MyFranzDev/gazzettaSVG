#!/usr/bin/env python3
"""Test script per verificare il comportamento con testi lunghi"""

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

# Test con testi molto lunghi
engine.set_content_data({
    'header_text': 'PROMO FLASH SUPER ESCLUSIVA',
    'main_title': 'IMPRESA STRAORDINARIA BOLOGNA CHAMPIONS',
    'cta_text': 'ABBONATI SUBITO ORA',
    'price': '14,99€',
    'price_period': '/ANNO',
    'logo_small_dark': f'data:image/png;base64,{logo_data}'
})

# Carica background
with open('background/bg15.png', 'rb') as f:
    bg_data = base64.b64encode(f.read()).decode('utf-8')

engine.set_background({
    'image_data': bg_data,
    'color': '#8B0000'
})

# Renderizza
svg = engine.render_template(template)

# Salva
with open('output/test_728x90_long_text.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print('✅ Generato: output/test_728x90_long_text.svg')
print('   Test con testi lunghi:')
print('   - Header: "PROMO FLASH SUPER ESCLUSIVA"')
print('   - Title: "IMPRESA STRAORDINARIA BOLOGNA CHAMPIONS"')
print('   - CTA: "ABBONATI SUBITO ORA"')
