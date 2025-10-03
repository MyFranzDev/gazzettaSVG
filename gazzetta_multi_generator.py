#!/usr/bin/env python3
"""
Gazzetta Multi-Banner SVG Generator
Generates multiple SVG banners from JSON templates with AI-powered copywriting
"""

import os
import sys
import base64
import json
from openai import OpenAI
from template_engine import TemplateEngine, load_template, save_svg


def step1_get_parameters():
    """STEP 1: Raccolta parametri evento e sport"""
    print("\n" + "=" * 60)
    print("STEP 1: PARAMETRI EVENTO E SPORT")
    print("=" * 60)

    event_type = input("Evento [Tennis - US Open]: ").strip() or "Tennis - US Open"
    price = input("Prezzo [0,99€ / mese]: ").strip() or "0,99€ / mese"

    print("\nSport:")
    sports = [
        "Calcio",
        "Tennis",
        "Pallavolo/Volley",
        "Ciclismo",
        "Golf",
        "Formula 1/Moto GP",
        "Generico",
        "Altro (scrivi manualmente)"
    ]

    for i, sport in enumerate(sports, 1):
        print(f"  {i}. {sport}")

    sport_choice = input(f"\nScegli sport [1-{len(sports)}]: ").strip() or "7"
    sport_idx = int(sport_choice) - 1

    if sport_idx == len(sports) - 1:  # "Altro"
        selected_sport = input("Inserisci sport manualmente: ").strip() or "Generico"
    else:
        selected_sport = sports[sport_idx]

    print(f"✅ Sport selezionato: {selected_sport}")

    return {
        "event_type": event_type,
        "price": price,
        "sport": selected_sport
    }


def step2_generate_texts(params):
    """STEP 2: Generazione testi con AI"""
    print("\n" + "=" * 60)
    print("STEP 2: GENERAZIONE TESTI AI")
    print("=" * 60)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable. Set it with: export OPENAI_API_KEY='your-key'")

    client = OpenAI(api_key=api_key)

    prompt = f"""
Sei un copywriter per La Gazzetta dello Sport.
Evento: {params['event_type']}

Genera 3 varianti di copy per un banner promozionale:

1. FOMO (urgenza, occasione limitata)
2. Esclusiva (premium, riservata)
3. Soft (amichevole, inclusiva)

Per ogni variante genera:
- Header (breve, 3-5 parole)
- Main Title (accattivante, 6-10 parole)
- Subtitle (dettaglio, 6-10 parole)
- CTA (call to action, massimo 4 parole)

Formato JSON:
{{
  "variant_1_fomo": {{
    "header": "...",
    "main_title": "...",
    "subtitle": "...",
    "cta": "..."
  }},
  "variant_2_esclusiva": {{...}},
  "variant_3_soft": {{...}}
}}
"""

    print("🤖 Generazione testi in corso...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sei un copywriter esperto. Rispondi SOLO con JSON valido."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    raw_response = response.choices[0].message.content.strip()

    # Clean JSON if wrapped in markdown code blocks
    if raw_response.startswith("```"):
        raw_response = raw_response.split("```")[1]
        if raw_response.startswith("json"):
            raw_response = raw_response[4:]
        raw_response = raw_response.strip()

    variants = json.loads(raw_response)

    print("\n✅ Testi generati:")
    for variant_name, texts in variants.items():
        print(f"\n{variant_name.upper()}:")
        for key, val in texts.items():
            print(f"  {key}: {val}")

    return variants


def step3_select_texts(variants):
    """STEP 3: Selezione varianti testi"""
    print("\n" + "=" * 60)
    print("STEP 3: SELEZIONE TESTI")
    print("=" * 60)

    variant_list = list(variants.keys())

    print("\nScegli la variante per ogni elemento:")

    choices = {}
    for field in ["header", "main_title", "subtitle", "cta"]:
        print(f"\n{field.upper()}:")
        for i, vname in enumerate(variant_list, 1):
            print(f"  {i}. {variants[vname][field]}")

        choice = input(f"Scegli [{', '.join(map(str, range(1, len(variant_list)+1)))}] (default=1): ").strip() or "1"
        selected_variant = variant_list[int(choice) - 1]
        choices[field] = variants[selected_variant][field]

    print("\n✅ Testi selezionati:")
    for k, v in choices.items():
        print(f"  {k}: {v}")

    return choices


def step4_load_resources(params):
    """STEP 4: Caricamento risorse (immagine utente, background)"""
    print("\n" + "=" * 60)
    print("STEP 4: CARICAMENTO RISORSE")
    print("=" * 60)

    # User image
    image_path = input("\nPath immagine opzionale (invio per saltare): ").strip()

    user_image = None
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            img_bytes = f.read()
            b64 = base64.b64encode(img_bytes).decode("utf-8")

            ext = image_path.lower().split('.')[-1]
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"

            user_image = f"data:{mime};base64,{b64}"
            print(f"✅ Immagine caricata: {image_path}")
    else:
        print("⏭️  Nessuna immagine caricata")

    # Background selection by sport
    print("\n🎨 Selezione background...")

    # Background catalog organized by sport
    backgrounds_catalog = {
        "Generico": [
            {"name": "Sfondo 1", "file": "bg01.png", "color": "#223047"},
            {"name": "Sfondo 2", "file": "bg02.png", "color": "#223047"},
            {"name": "Sfondo 3", "file": "bg03.png", "color": "#223047"}
        ],
        "Pallavolo/Volley": [
            {"name": "Volley 1", "file": "bg06.png", "color": "#cc0000"},
            {"name": "Volley 2", "file": "bg07.png", "color": "#cc0000"},
            {"name": "Volley 3", "file": "bg08.png", "color": "#cc0000"},
            {"name": "Volley 4", "file": "bg09.png", "color": "#cc0000"},
            {"name": "Volley 5", "file": "bg10.png", "color": "#cc0000"}
        ],
        "Tennis": [
            {"name": "Wimbledon", "file": "bg11.png", "color": "#006633"},
            {"name": "US Open", "file": "bg12.png", "color": "#0066cc"}
        ],
        "Ciclismo": [
            {"name": "Ciclismo", "file": "bg14.png", "color": "#FFD700"}
        ],
        "Calcio": [
            {"name": "Champions League 1", "file": "bg15.png", "color": "#003399"},
            {"name": "Champions League 2", "file": "bg16.png", "color": "#003399"},
            {"name": "Champions League 3", "file": "bg17.png", "color": "#003399"},
            {"name": "Generico 1", "file": "bg18.png", "color": "#0066cc"},
            {"name": "Generico 2", "file": "bg19.png", "color": "#0066cc"},
            {"name": "Generico 3", "file": "bg20.png", "color": "#0066cc"},
            {"name": "Generico 4", "file": "bg22.png", "color": "#0066cc"},
            {"name": "Generico 5", "file": "bg23.png", "color": "#0066cc"},
            {"name": "Generico 6", "file": "bg24.png", "color": "#0066cc"}
        ],
        "Golf": [
            {"name": "Golf 1", "file": "bg21.png", "color": "#228B22"},
            {"name": "Golf 2", "file": "bg13.png", "color": "#228B22"}
        ],
        "Formula 1/Moto GP": [
            {"name": "F1/MotoGP 1", "file": "bg25.png", "color": "#E10600"},
            {"name": "F1/MotoGP 2", "file": "bg26.png", "color": "#E10600"},
            {"name": "F1/MotoGP 3", "file": "bg27.png", "color": "#E10600"},
            {"name": "F1/MotoGP 4", "file": "bg28.png", "color": "#E10600"},
            {"name": "F1/MotoGP 5", "file": "bg29.png", "color": "#E10600"}
        ]
    }

    # Get backgrounds for selected sport
    selected_sport = params.get("sport", "Generico")
    sport_backgrounds = backgrounds_catalog.get(selected_sport, backgrounds_catalog["Generico"])

    print(f"\nBackground disponibili per {selected_sport}:")
    for i, bg in enumerate(sport_backgrounds, 1):
        print(f"  {i}. {bg['file']} - {bg['name']}")

    bg_choice = input(f"\nScegli background [1-{len(sport_backgrounds)}] (default=1): ").strip() or "1"
    chosen_bg = sport_backgrounds[int(bg_choice) - 1]

    # Load and encode background
    try:
        bg_path = os.path.join("background", chosen_bg["file"])
        with open(bg_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            mime = "image/jpeg" if chosen_bg["file"].endswith((".jpg", ".jpeg")) else "image/png"

            chosen = {
                "image": f"data:{mime};base64,{b64}",
                "main_color": chosen_bg["color"],
                "dark_color": chosen_bg["color"]
            }
            print(f"✅ Background: {chosen_bg['file']} ({chosen_bg['name']})")
    except FileNotFoundError:
        print(f"⚠️ File {chosen_bg['file']} non trovato, sfondo disabilitato")
        chosen = {
            "image": None,
            "main_color": chosen_bg["color"],
            "dark_color": chosen_bg["color"]
        }

    return {
        "user_image": user_image,
        "background": chosen
    }


def step5_select_templates():
    """STEP 5: Selezione template da generare"""
    print("\n" + "=" * 60)
    print("STEP 5: SELEZIONE TEMPLATE")
    print("=" * 60)

    templates_dir = "templates"
    template_files = sorted([f for f in os.listdir(templates_dir) if f.endswith(".json")])

    if not template_files:
        raise FileNotFoundError(f"No templates found in {templates_dir}/")

    print("\nTemplate disponibili:")
    for i, tfile in enumerate(template_files, 1):
        tname = tfile.replace(".json", "")
        print(f"  {i}. {tname}")

    print(f"  {len(template_files) + 1}. TUTTI")

    choice = input(f"\nScegli template [1-{len(template_files) + 1}] o numeri separati da virgola (es. 1,3,5): ").strip()

    if choice == str(len(template_files) + 1) or choice.lower() == "tutti":
        selected = template_files
    elif "," in choice:
        indices = [int(x.strip()) - 1 for x in choice.split(",")]
        selected = [template_files[i] for i in indices]
    else:
        selected = [template_files[int(choice) - 1]]

    print(f"\n✅ Selezionati {len(selected)} template")

    return selected


def step6_render_banners(templates, texts, resources, params):
    """STEP 6: Rendering multi-banner"""
    print("\n" + "=" * 60)
    print("STEP 6: RENDERING BANNERS")
    print("=" * 60)

    # Prepare content data
    content_data = {
        "header_text": texts.get("header", ""),
        "main_title": texts.get("main_title", ""),
        "subtitle": texts.get("subtitle", ""),
        "cta_text": f"{texts.get('cta', '')} a {params['price']}",
        "user_image": resources.get("user_image", ""),
        "bullet1": "✓ Contenuti e Speciali esclusivi",
        "bullet2": "✓ Analisi e interviste",
        "bullet3": "✓ Il meglio delle grandi firme de La Gazzetta dello Sport"
    }

    # Initialize engine
    engine = TemplateEngine()
    engine.load_fonts()
    engine.set_content_data(content_data)
    engine.set_background(resources.get("background", {}))

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n🚀 Generazione {len(templates)} banner in corso...")

    for template_file in templates:
        template_path = os.path.join("templates", template_file)
        template = load_template(template_path)

        svg_content = engine.render_template(template)

        output_file = os.path.join(output_dir, template_file.replace(".json", ".svg"))
        save_svg(svg_content, output_file)

    print(f"\n✅ Completato! {len(templates)} banner generati in '{output_dir}/'")


def main():
    """Main workflow"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║   GAZZETTA MULTI-BANNER SVG GENERATOR                     ║
║   Template-driven architecture for scalable banner gen    ║
╚═══════════════════════════════════════════════════════════╝
""")

    try:
        # Step 1: Parameters
        params = step1_get_parameters()

        # Step 2: AI text generation
        variants = step2_generate_texts(params)

        # Step 3: Text selection
        texts = step3_select_texts(variants)

        # Step 4: Load resources
        resources = step4_load_resources(params)

        # Step 5: Select templates
        templates = step5_select_templates()

        # Step 6: Render banners
        step6_render_banners(templates, texts, resources, params)

        print("\n🎉 Processo completato con successo!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Processo interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
