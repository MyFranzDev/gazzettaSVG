#!/usr/bin/env python3
"""
Gazzetta SVG Banner Generator
Convertito da notebook Jupyter a script procedurale
"""

import os
import json
import base64
import random
import copy
from openai import OpenAI


# ============================================================================
# STEP 1: RACCOLTA PARAMETRI
# ============================================================================
def step1_get_parameters():
    """Raccoglie i parametri base per il banner"""
    print("\n" + "="*60)
    print("STEP 1: PARAMETRI BANNER")
    print("="*60)

    event_type = input("Evento [Calcio - Finale Champions League]: ").strip() or "Calcio - Finale Champions League"
    price = input("Prezzo [14,99€ / ANNO]: ").strip() or "14,99€ / ANNO"
    width = input("Larghezza [600]: ").strip() or "600"
    height = input("Altezza [500]: ").strip() or "500"

    try:
        width = int(width)
    except:
        width = 600

    try:
        height = int(height)
    except:
        height = 500

    print(f"\n✅ Parametri confermati:")
    print(f"   Evento: {event_type}")
    print(f"   Prezzo: {price}")
    print(f"   Dimensioni: {width}x{height}")

    return {
        "event_type": event_type,
        "price": price,
        "width": width,
        "height": height
    }


# ============================================================================
# STEP 2: GENERAZIONE TESTI CON OPENAI
# ============================================================================
def step2_generate_texts(event_type):
    """Genera 3 varianti di testi usando OpenAI"""
    print("\n" + "="*60)
    print("STEP 2: GENERAZIONE TESTI")
    print("="*60)

    # API Key (DEVE essere impostata come variabile d'ambiente: export OPENAI_API_KEY='your-key')
    if "OPENAI_API_KEY" not in os.environ:
        print("⚠️  ERRORE: Variabile d'ambiente OPENAI_API_KEY non impostata")
        print("   Imposta la chiave con: export OPENAI_API_KEY='your-key'")
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    client = OpenAI()

    prompt = f"""
    Sei un copywriter pubblicitario per G+, piattaforma di contenuti sportivi premium.
    Evento: {event_type}

    Genera ESATTAMENTE 3 varianti con toni diversi:
    1) FOMO → urgenza, occasione limitata
    2) Esclusiva → premium, riservata
    3) Soft → amichevole, inclusiva

    Ogni variante deve contenere:
    - style (esattamente "FOMO", "Esclusiva" o "Soft")
    - header (max 3 parole, es: "PROMO FLASH", "ESCLUSIVA G+")
    - main_title (titolo evento max 4 parole)
    - subtitle_text (max 10 parole)
    - cta_text (CTA breve: "ABBONATI", "ABBONATI ORA", "ATTIVA SUBITO", "NON PERDERE L'OCCASIONE")

    ✅ Rispondi SOLO con JSON, senza testo extra.
    ✅ Esempio di formato corretto (contenuti puramente indicativi):

    [
      {{
        "style": "FOMO",
        "header": "PROMO FLASH",
        "main_title": "Finale Volley",
        "subtitle_text": "Ultima occasione su G+",
        "cta_text": "ABBONATI ORA"
      }},
      {{
        "style": "Esclusiva",
        "header": "ESCLUSIVA G+",
        "main_title": "US OPEN",
        "subtitle_text": "Solo per i veri fan",
        "cta_text": "ATTIVA SUBITO"
      }},
      {{
        "style": "Soft",
        "header": "SPECIAL PASS",
        "main_title": "NBA Finals",
        "subtitle_text": "Seguilo con la community",
        "cta_text": "ABBONATI"
      }}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Genera testi pubblicitari brevi per banner promozionali."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            max_tokens=500
        )

        texts = json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"⚠️  Errore generazione testi: {e}")
        print("   Uso testi di fallback...")
        texts = [
            {
                "style": "FOMO",
                "header": "PROMO",
                "main_title": event_type,
                "subtitle_text": "Non perderti l'evento!",
                "cta_text": "ABBONATI ORA"
            },
            {
                "style": "Esclusiva",
                "header": "ESCLUSIVA G+",
                "main_title": event_type,
                "subtitle_text": "Solo su G+",
                "cta_text": "ATTIVA SUBITO"
            },
            {
                "style": "Soft",
                "header": "PASS SPECIALE",
                "main_title": event_type,
                "subtitle_text": "Seguilo con noi",
                "cta_text": "ABBONATI"
            }
        ]

    print(f"\n✅ Testi generati per: {event_type}")
    for i, t in enumerate(texts, start=1):
        print(f"\nVariante {i} ({t['style']}):")
        print(f"   Header: {t['header']}")
        print(f"   Main Title: {t['main_title']}")
        print(f"   Subtitle: {t['subtitle_text']}")
        print(f"   CTA: {t['cta_text']}")

    return texts


# ============================================================================
# STEP 3: SELEZIONE TEMPLATE E TESTI
# ============================================================================
def step3_select_template_and_texts(texts):
    """Selezione template e testi (versione CLI)"""
    print("\n" + "="*60)
    print("STEP 3: SELEZIONE TEMPLATE E TESTI")
    print("="*60)

    # Template disponibile (puoi aggiungerne altri)
    template_base = {
        "width": 500,
        "height": 500,
        "header": {
            "text": "",
            "background": "#223047",
            "color": "#FFFFFF",
            "font_family": "Oswald",
            "font_weight": "700",
            "align": "center",
            "height_ratio": 0.2
        },
        "main_title": {
            "text": "",
            "color": "#FFFFFF",
            "font_family": "Roboto",
            "font_weight": "700",
            "align": "center",
            "height_ratio": 0.1
        },
        "body": {
            "background": {},
            "left": {
                "image": None,
                "width_ratio": 0.4,
                "margin": 10
            },
            "right": {
                "subtitle_text": {
                    "text": "",
                    "color": "#FFFFFF",
                    "font_family": "Roboto",
                    "font_weight": "400",
                    "align": "left",
                    "line_height": 1.2
                },
                "price_text": {
                    "text": "9.99€",
                    "color": "#FFD700",
                    "font_family": "Roboto",
                    "font_weight": "700",
                    "align": "left",
                    "font_size_ratio": 0.08
                },
                "cta_text": {
                    "text": "",
                    "background": "#FFD700",
                    "color": "#000000",
                    "font_family": "Roboto",
                    "font_weight": "700",
                    "align": "center",
                    "padding": 10,
                    "border_radius": 8
                }
            }
        },
        "footer": {
            "text": "Gazzetta dello Sport",
            "color": "#FFFFFF",
            "background": "#223047",
            "font_family": "Roboto",
            "font_weight": "400",
            "align": "right-column",
            "height_ratio": 0.1
        }
    }

    # Selezione testi
    print("\nScegli la variante per ogni elemento:")
    print("\nVARIANTI DISPONIBILI:")
    for i, t in enumerate(texts, start=1):
        print(f"{i}. {t['style']}: {t['header']} | {t['main_title']} | {t['subtitle_text']} | {t['cta_text']}")

    print("\n")
    header_choice = input(f"Header [1-{len(texts)}, default=1]: ").strip() or "1"
    main_title_choice = input(f"Main Title [1-{len(texts)}, default=1]: ").strip() or "1"
    subtitle_choice = input(f"Subtitle [1-{len(texts)}, default=1]: ").strip() or "1"
    cta_choice = input(f"CTA [1-{len(texts)}, default=1]: ").strip() or "1"

    try:
        header_idx = int(header_choice) - 1
        if header_idx < 0 or header_idx >= len(texts):
            header_idx = 0
    except:
        header_idx = 0

    try:
        main_title_idx = int(main_title_choice) - 1
        if main_title_idx < 0 or main_title_idx >= len(texts):
            main_title_idx = 0
    except:
        main_title_idx = 0

    try:
        subtitle_idx = int(subtitle_choice) - 1
        if subtitle_idx < 0 or subtitle_idx >= len(texts):
            subtitle_idx = 0
    except:
        subtitle_idx = 0

    try:
        cta_idx = int(cta_choice) - 1
        if cta_idx < 0 or cta_idx >= len(texts):
            cta_idx = 0
    except:
        cta_idx = 0

    texts_selected = {
        "header": texts[header_idx]["header"],
        "main_title": texts[main_title_idx]["main_title"],
        "subtitle_text": texts[subtitle_idx]["subtitle_text"],
        "cta_text": texts[cta_idx]["cta_text"]
    }

    # Immagine opzionale
    print("\n")
    image_path = input("Path immagine opzionale (invio per saltare): ").strip()
    uploaded_image = None
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as f:
                uploaded_bytes = f.read()
                uploaded_b64 = base64.b64encode(uploaded_bytes).decode("utf-8")
                # Rileva formato immagine
                ext = image_path.lower().split('.')[-1]
                mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
                uploaded_image = f"data:{mime_type};base64,{uploaded_b64}"
            print(f"✅ Immagine caricata: {image_path}")
        except Exception as e:
            print(f"⚠️  Errore caricamento immagine: {e}")

    # Mockup
    mockup_mode = "none"
    mockup_input = input("Mostra immagine dentro smartphone? (s/n, default=n): ").strip().lower()
    if mockup_input == "s":
        mockup_mode = "smartphone"

    print("\n✅ Scelte confermate:")
    print(f"   Header: {texts_selected['header']}")
    print(f"   Main Title: {texts_selected['main_title']}")
    print(f"   Subtitle: {texts_selected['subtitle_text']}")
    print(f"   CTA: {texts_selected['cta_text']}")
    print(f"   Immagine: {'Presente' if uploaded_image else 'Nessuna'}")
    print(f"   Mockup: {mockup_mode}")

    return {
        "template_base": template_base,
        "texts_selected": texts_selected,
        "uploaded_image": uploaded_image,
        "mockup_mode": mockup_mode
    }


# ============================================================================
# STEP 4: SELEZIONE AUTOMATICA SFONDO
# ============================================================================
def step4_pick_background(event_type):
    """Seleziona automaticamente lo sfondo in base all'evento"""
    print("\n" + "="*60)
    print("STEP 4: SELEZIONE SFONDO")
    print("="*60)

    # Database sfondi (mock - in produzione usa file reali)
    backgrounds = [
        # Calcio
        {"sport": "calcio", "competition": "champions league", "image": "bg15.png", "main_color": "#052d97", "dark_color": "#00073b"},
        {"sport": "calcio", "competition": "champions league", "image": "bg16.png", "main_color": "#052d97", "dark_color": "#00073b"},
        {"sport": "calcio", "competition": "champions league", "image": "bg17.png", "main_color": "#052d97", "dark_color": "#00073b"},

        {"sport": "calcio", "competition": "serie a", "image": "bg_seriea_1.png", "main_color": "#0066b2", "dark_color": "#00334d"},
        {"sport": "calcio", "competition": "serie a", "image": "bg_seriea_2.png", "main_color": "#0066b2", "dark_color": "#00334d"},
        {"sport": "calcio", "competition": "serie a", "image": "bg_seriea_3.png", "main_color": "#0066b2", "dark_color": "#00334d"},

        {"sport": "calcio", "competition": "coppa italia", "image": "bg_coppa_1.png", "main_color": "#1b8a5a", "dark_color": "#0d4430"},
        {"sport": "calcio", "competition": "coppa italia", "image": "bg_coppa_2.png", "main_color": "#1b8a5a", "dark_color": "#0d4430"},
        {"sport": "calcio", "competition": "coppa italia", "image": "bg_coppa_3.png", "main_color": "#1b8a5a", "dark_color": "#0d4430"},

        # Tennis
        {"sport": "tennis", "competition": "wimbledon", "image": "bg_wimbledon_1.png", "main_color": "#2e8b57", "dark_color": "#145c32"},
        {"sport": "tennis", "competition": "wimbledon", "image": "bg_wimbledon_2.png", "main_color": "#2e8b57", "dark_color": "#145c32"},
        {"sport": "tennis", "competition": "wimbledon", "image": "bg_wimbledon_3.png", "main_color": "#2e8b57", "dark_color": "#145c32"},

        {"sport": "tennis", "competition": "roland garros", "image": "bg_rg_1.png", "main_color": "#b7410e", "dark_color": "#5a2007"},
        {"sport": "tennis", "competition": "roland garros", "image": "bg_rg_2.png", "main_color": "#b7410e", "dark_color": "#5a2007"},
        {"sport": "tennis", "competition": "roland garros", "image": "bg_rg_3.png", "main_color": "#b7410e", "dark_color": "#5a2007"},

        {"sport": "tennis", "competition": "us open", "image": "bg04.png", "main_color": "#ffcc00", "dark_color": "#806600"},
        {"sport": "tennis", "competition": "us open", "image": "bg_usopen_2.png", "main_color": "#ffcc00", "dark_color": "#806600"},
        {"sport": "tennis", "competition": "us open", "image": "bg_usopen_3.png", "main_color": "#ffcc00", "dark_color": "#806600"},

        # Volley
        {"sport": "volley", "competition": "volley", "image": "bg07.png", "main_color": "#e63946", "dark_color": "#7a1a20"},
        {"sport": "volley", "competition": "volley", "image": "bg_wimbledon_2.png", "main_color": "#e63946", "dark_color": "#7a1a20"},
        {"sport": "volley", "competition": "volley", "image": "bg_wimbledon_3.png", "main_color": "#e63946", "dark_color": "#7a1a20"},

        # Default
        {"sport": "default", "competition": "default", "image": "bg01.png", "main_color": "#444444", "dark_color": "#222222"},
        {"sport": "default", "competition": "default", "image": "bg02.png", "main_color": "#444444", "dark_color": "#222222"},
        {"sport": "default", "competition": "default", "image": "bg03.png", "main_color": "#444444", "dark_color": "#222222"},
        {"sport": "default", "competition": "default", "image": "bg06.png", "main_color": "#444444", "dark_color": "#222222"},
        {"sport": "default", "competition": "default", "image": "bg07.png", "main_color": "#444444", "dark_color": "#222222"}
    ]

    event_lower = event_type.lower()

    # Match competition
    candidates = [bg for bg in backgrounds if bg["competition"] in event_lower]
    if not candidates:
        # Match sport
        candidates = [bg for bg in backgrounds if bg["sport"] in event_lower]
    if not candidates:
        # Fallback default
        candidates = [bg for bg in backgrounds if bg["sport"] == "default"]

    chosen = random.choice(candidates)
    chosen_bg = copy.deepcopy(chosen)

    # Converti immagine in base64 (se esiste)
    try:
        bg_path = os.path.join("background", chosen["image"])
        with open(bg_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            if chosen["image"].endswith(".png"):
                mime = "image/png"
            elif chosen["image"].endswith(".jpg") or chosen["image"].endswith(".jpeg"):
                mime = "image/jpeg"
            else:
                mime = "image/png"
            chosen_bg["image"] = f"data:{mime};base64,{b64}"
    except FileNotFoundError:
        print(f"⚠️  File {chosen['image']} non trovato, sfondo disabilitato")
        chosen_bg["image"] = None

    print(f"\n✅ Sfondo selezionato automaticamente:")
    print(f"   Sport: {chosen_bg['sport']}")
    print(f"   Competition: {chosen_bg['competition']}")
    print(f"   Colore principale: {chosen_bg['main_color']}")
    print(f"   Colore scuro: {chosen_bg['dark_color']}")

    return chosen_bg


# ============================================================================
# STEP 5: COSTRUZIONE TEMPLATE FINALE
# ============================================================================
def step5_build_final_template(template_base, texts_selected, uploaded_image, mockup_mode, chosen_bg, price):
    """Assembla il template finale con tutti i dati"""
    print("\n" + "="*60)
    print("STEP 5: ASSEMBLAGGIO TEMPLATE FINALE")
    print("="*60)

    final_template = copy.deepcopy(template_base)

    # Inserisci testi
    final_template["header"]["text"] = texts_selected["header"]
    final_template["main_title"]["text"] = texts_selected["main_title"]
    final_template["body"]["right"]["subtitle_text"]["text"] = texts_selected["subtitle_text"]
    final_template["body"]["right"]["price_text"]["text"] = price
    final_template["body"]["right"]["cta_text"]["text"] = texts_selected["cta_text"]

    # Immagine + mockup
    final_template["body"]["left"]["image"] = uploaded_image
    final_template["body"]["left"]["mockup"] = mockup_mode

    # Background
    final_template["body"]["background"] = {
        "type": "image",
        "image": chosen_bg["image"],
        "sport": chosen_bg["sport"],
        "competition": chosen_bg["competition"]
    }

    # Override colori header/footer
    final_template["header"]["background"] = chosen_bg["dark_color"]
    final_template["footer"]["background"] = chosen_bg["dark_color"]

    print("\n✅ Template finale assemblato")

    return final_template


# ============================================================================
# STEP 6: RENDERING SVG
# ============================================================================
def step6_render_svg(template, width, height, out_path="banner.svg"):
    """Renderizza il template in SVG"""
    print("\n" + "="*60)
    print("STEP 6: RENDERING SVG")
    print("="*60)

    # Carica font embedded
    def font_to_base64(path):
        full_path = os.path.join("font", path)
        with open(full_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # Prova a caricare i font (fallback se non esistono)
    try:
        oswald_bold_b64 = font_to_base64("Oswald-Bold.woff2")
        roboto_regular_b64 = font_to_base64("Roboto-Regular.woff2")
        roboto_bold_b64 = font_to_base64("Roboto-Bold.woff2")

        font_style_block = f"""
<style type="text/css">
  @font-face {{
    font-family: 'Oswald';
    font-style: normal;
    font-weight: 700;
    src: url(data:font/woff2;base64,{oswald_bold_b64}) format('woff2');
  }}
  @font-face {{
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 400;
    src: url(data:font/woff2;base64,{roboto_regular_b64}) format('woff2');
  }}
  @font-face {{
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 700;
    src: url(data:font/woff2;base64,{roboto_bold_b64}) format('woff2');
  }}

  .font-header {{ font-family: 'Oswald', sans-serif; font-weight: 700; }}
  .font-body   {{ font-family: 'Roboto', sans-serif; }}
</style>
"""
    except FileNotFoundError as e:
        print(f"⚠️  Font non trovati ({e}), uso font di sistema")
        font_style_block = """
<style type="text/css">
  .font-header { font-family: 'Arial Black', sans-serif; font-weight: 700; }
  .font-body   { font-family: 'Arial', sans-serif; }
</style>
"""

    # Override dimensioni template
    template["width"] = width
    template["height"] = height

    W = template["width"]
    H = template["height"]

    # Calcoli sezioni
    header_h = int(H * template["header"]["height_ratio"])
    main_title_h = int(H * template["main_title"]["height_ratio"])
    footer_h = int(H * template["footer"]["height_ratio"])

    body_y = header_h
    body_h = max(0, H - header_h - footer_h)

    body_left_w = int(W * template["body"]["left"]["width_ratio"])
    gutter = template["body"]["left"].get("margin", 10)
    body_right_x = body_left_w + gutter
    body_right_w = max(0, W - body_right_x - gutter)

    # Testi principali
    header_text = template["header"]["text"]
    main_title_text = template["main_title"]["text"]
    subtitle_text = template["body"]["right"]["subtitle_text"]["text"]
    price_text = template["body"]["right"]["price_text"]["text"]
    cta_text = template["body"]["right"]["cta_text"]["text"]
    footer_text = template["footer"]["text"]

    # Colori/background
    header_bg = template["header"]["background"]
    header_color = template["header"]["color"]
    main_title_color = template["main_title"]["color"]
    subtitle_color = template["body"]["right"]["subtitle_text"]["color"]
    cta_bg = template["body"]["right"]["cta_text"]["background"]
    cta_color = template["body"]["right"]["cta_text"]["color"]
    footer_color = template["footer"]["color"]
    footer_bg = template["footer"].get("background", "none")

    cta_padding = template["body"]["right"]["cta_text"].get("padding", 10)
    cta_radius = template["body"]["right"]["cta_text"].get("border_radius", 8)

    left_image = template["body"]["left"]["image"]
    body_bg_image = template["body"]["background"].get("image")

    def esc(txt):
        return (txt or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&apos;")

    def wrap_text(text, max_width, font_size):
        words = (text or "").split()
        lines, current = [], []
        for w in words:
            test_line = current + [w]
            approx_w = len(" ".join(test_line)) * (font_size * 0.6)
            if approx_w <= max_width:
                current = test_line
            else:
                if current:
                    lines.append(" ".join(current))
                current = [w]
        if current:
            lines.append(" ".join(current))
        if not lines:
            lines = [""]
        return lines

    svg = []
    svg.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">')
    svg.append(font_style_block)

    # --- HEADER ---
    svg.append(f'<rect x="0" y="0" width="{W}" height="{header_h}" fill="{header_bg}"/>')
    max_header_fs = int(header_h * 0.75)
    approx_header_width = len(header_text) * (max_header_fs * 0.6)
    header_fs = int((W * 0.9) / (len(header_text) * 0.6)) if len(header_text) and approx_header_width > W * 0.9 else max_header_fs
    svg.append(f'''
    <text x="{W/2}" y="{header_h/2 + header_fs*0.1}"
          text-anchor="middle" dominant-baseline="middle"
          class="font-header" fill="{header_color}"
          font-size="{header_fs}">{esc(header_text)}</text>
    ''')

    # --- BODY BACKGROUND ---
    if body_bg_image:
        # body_bg_image è già un data URI (convertito nello STEP 4)
        svg.append(f'<image href="{body_bg_image}" x="0" y="{body_y}" width="{W}" height="{body_h}" preserveAspectRatio="xMidYMid slice"/>')
    else:
        svg.append(f'<rect x="0" y="{body_y}" width="{W}" height="{body_h}" fill="none"/>')

    # --- MAIN TITLE ---
    max_title_fs = int(main_title_h * 0.75)
    approx_title_w = len(main_title_text) * (max_title_fs * 0.6)
    title_fs = int((W * 0.9) / (len(main_title_text) * 0.6)) if len(main_title_text) and approx_title_w > W * 0.9 else max_title_fs
    svg.append(f'''
    <text x="{W/2}" y="{body_y + main_title_h/2 + title_fs*0.1}"
          text-anchor="middle" dominant-baseline="middle"
          class="font-body" fill="{main_title_color}"
          font-size="{title_fs}" font-weight="700">{esc(main_title_text)}</text>
    ''')

    # --- BODY LEFT ---
    body_side_margin = 30
    left_content_w = body_left_w - body_side_margin - gutter

    if left_image:
        svg.append(f'<image href="{esc(left_image)}" x="{body_side_margin}" y="{body_y + gutter + main_title_h}" width="{left_content_w}" height="{body_h - gutter*2 - main_title_h}" preserveAspectRatio="xMidYMid slice" />')
    else:
        svg.append(f'<rect x="{body_side_margin}" y="{body_y + gutter + main_title_h}" width="{left_content_w}" height="{body_h - gutter*2 - main_title_h}" fill="rgba(255,255,255,0.06)"/>')

    # --- BODY RIGHT ---
    right_x = body_right_x
    body_right_y = body_y + main_title_h + gutter
    footer_y = H - footer_h
    padding_top = int(H * 0.05)
    padding_bottom = int(H * 0.05)
    body_right_h = footer_y - body_right_y - gutter - padding_top - padding_bottom

    # Calcola dimensioni elementi
    subtitle_fs = int(body_right_h * 0.15)
    max_width = (W - body_right_x - body_side_margin) * 0.9
    body_right_w_effective = W - body_right_x - body_side_margin

    lines = wrap_text(subtitle_text, max_width, subtitle_fs)
    line_height = int(subtitle_fs * 1.2)
    subtitle_block_h = max(line_height * len(lines), subtitle_fs)

    max_price_fs = int(body_right_h * 0.25)
    approx_price_w = len(price_text) * (max_price_fs * 0.6) if price_text else 0
    price_fs = int((body_right_w_effective * 0.9) / (len(price_text) * 0.6)) if price_text and approx_price_w > body_right_w_effective * 0.9 else max_price_fs
    price_block_h = int(price_fs * 1.1)

    cta_fs = int(body_right_h * 0.12)
    cta_w = body_right_w_effective
    cta_h = cta_fs + cta_padding*2

    section_h = body_right_h / 3
    start_y = body_right_y + padding_top

    # SUBTITLE (sezione 1)
    subtitle_y0 = start_y + (section_h - subtitle_block_h) / 2 + subtitle_fs
    tspans = []
    for i, line in enumerate(lines):
        dy = line_height if i > 0 else 0
        tspans.append(f'<tspan x="{right_x + body_right_w_effective/2}" dy="{dy}">{esc(line)}</tspan>')
    svg.append(f'''
    <text x="{right_x + body_right_w_effective/2}" y="{subtitle_y0}"
          text-anchor="middle" class="font-body"
          fill="{subtitle_color}" font-size="{subtitle_fs}" font-weight="400">
      {''.join(tspans)}
    </text>
    ''')

    # PRICE (sezione 2)
    price_y = start_y + section_h + (section_h - price_block_h) / 2 + price_fs
    svg.append(f'''
    <text x="{right_x + body_right_w_effective/2}" y="{price_y}"
          text-anchor="middle"
          class="font-body" fill="#FFFFFF"
          font-size="{price_fs}" font-weight="700">{esc(price_text)}</text>
    ''')

    # CTA (sezione 3)
    cta_y = start_y + section_h * 2 + (section_h - cta_h) / 2
    cta_x = right_x
    svg.append(f'<rect x="{cta_x}" y="{cta_y}" width="{cta_w}" height="{cta_h}" rx="{cta_radius}" ry="{cta_radius}" fill="{cta_bg}"/>')
    svg.append(f'''
    <text x="{cta_x + cta_w/2}" y="{cta_y + cta_h/2 + cta_fs*0.1}"
          text-anchor="middle" dominant-baseline="middle"
          class="font-body" fill="{cta_color}"
          font-size="{cta_fs}" font-weight="700">{esc(cta_text)}</text>
    ''')

    # --- FOOTER ---
    footer_y = H - footer_h
    if footer_bg != "none":
        svg.append(f'<rect x="0" y="{footer_y}" width="{W}" height="{footer_h}" fill="{footer_bg}"/>')

    footer_align = template["footer"].get("align", "center")
    footer_fs = int(footer_h * 0.5)

    def footer_x_for_align(al):
        if al == "left": return 10
        if al == "center": return W/2
        if al == "right": return W - 10
        if al == "left-column": return gutter
        if al == "right-column": return body_right_x + body_right_w - 10
        return W/2

    fx = footer_x_for_align(footer_align)
    anchor = "middle"
    if footer_align in ("left", "left-column"): anchor = "start"
    elif footer_align in ("right", "right-column"): anchor = "end"

    svg.append(f'<text x="{fx}" y="{footer_y + footer_h/2}" text-anchor="{anchor}" dominant-baseline="middle" class="font-body" fill="{footer_color}" font-size="{footer_fs}" font-weight="{template["footer"]["font_weight"]}">{esc(footer_text)}</text>')

    svg.append('</svg>')

    # Salva file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(svg))

    print(f"\n✅ SVG salvato: {os.path.abspath(out_path)}")
    return out_path


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("\n" + "="*60)
    print("GAZZETTA SVG BANNER GENERATOR")
    print("="*60)

    # Step 1: Parametri
    params = step1_get_parameters()

    # Step 2: Generazione testi
    texts = step2_generate_texts(params["event_type"])

    # Step 3: Selezione template e testi
    selections = step3_select_template_and_texts(texts)

    # Step 4: Selezione sfondo
    chosen_bg = step4_pick_background(params["event_type"])

    # Step 5: Template finale
    final_template = step5_build_final_template(
        selections["template_base"],
        selections["texts_selected"],
        selections["uploaded_image"],
        selections["mockup_mode"],
        chosen_bg,
        params["price"]
    )

    # Step 6: Render SVG
    output_file = step6_render_svg(final_template, params["width"], params["height"])

    print("\n" + "="*60)
    print("✅ GENERAZIONE COMPLETATA!")
    print(f"File creato: {output_file}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
