#!/usr/bin/env python3
"""Test script per generare 1920x1080 Full HD banner"""

from template_engine import TemplateEngine, load_template
import base64

# Inizializza engine
engine = TemplateEngine()
engine.load_fonts()

# Carica template 1920x1080
template = load_template('templates/1920x1080.json')

# Carica immagine smartphone (se esiste)
try:
    with open('images/smartphone_content.jpg', 'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
        user_image = f'data:image/jpeg;base64,{img_data}'
except FileNotFoundError:
    user_image = None
    print("ℹ️ Nessuna immagine trovata, verrà usato placeholder")

# Carica logo small (su sfondo scuro - bianco)
try:
    with open('images/G_bianco.png', 'rb') as f:
        logo_data = base64.b64encode(f.read()).decode('utf-8')
        logo_small = f'data:image/png;base64,{logo_data}'
except FileNotFoundError:
    logo_small = None
    print("⚠️ Logo G_bianco.png non trovato")

# Imposta dati di test
header_text = 'PROMO FLASH'
main_title = 'IMPRESA BOLOGNA'
header_title_combined = f'{header_text}: {main_title}'

engine.set_content_data({
    'header_title_combined': header_title_combined,
    'description_text': 'FESTEGGIA LA\nVITTORIA DEL\nBOLOGNA IN\nCOPPA ITALIA',
    'cta_text': 'ABBONATI',
    'price': '14,99€',
    'price_period': '/ANNO',
    'user_image': user_image,
    'logo_small_dark': logo_small
})

# Carica background
try:
    with open('background/bg15.png', 'rb') as f:
        bg_data = base64.b64encode(f.read()).decode('utf-8')
except FileNotFoundError:
    bg_data = None
    print("⚠️ Background bg15.png non trovato, verrà usato colore solido")

engine.set_background({
    'image_data': bg_data,
    'color': '#8B0000'  # Bordeaux fallback
})

# Renderizza
svg = engine.render_template(template)

# Salva
with open('output/test_1920x1080.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print('✅ Generato: output/test_1920x1080.svg')
print(f'   Dimensioni: {template["width"]}x{template["height"]}')
