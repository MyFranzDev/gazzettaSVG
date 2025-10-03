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
    """STEP 1: Raccolta parametri evento"""
    print("\n" + "=" * 60)
    print("STEP 1: PARAMETRI EVENTO")
    print("=" * 60)

    event_type = input("Evento [Tennis - US Open]: ").strip() or "Tennis - US Open"
    price = input("Prezzo [0,99€ / mese]: ").strip() or "0,99€ / mese"

    return {
        "event_type": event_type,
        "price": price
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

    # Background selection
    print("\n🎨 Selezione background automatica...")

    backgrounds = [
        {"sport": "calcio", "competition": "champions league", "image": "bg15.png", "main_color": "#003399", "dark_color": "#001a4d"},
        {"sport": "calcio", "competition": "serie a", "image": "bg01.png", "main_color": "#0066cc", "dark_color": "#003d7a"},
        {"sport": "calcio", "competition": "coppa italia", "image": "bg16.png", "main_color": "#009933", "dark_color": "#005c1f"},
        {"sport": "tennis", "competition": "wimbledon", "image": "bg17.png", "main_color": "#006633", "dark_color": "#003d1f"},
        {"sport": "tennis", "competition": "roland garros", "image": "bg18.png", "main_color": "#cc3300", "dark_color": "#7a1f00"},
        {"sport": "tennis", "competition": "us open", "image": "bg19.png", "main_color": "#0066cc", "dark_color": "#003d7a"},
        {"sport": "volley", "competition": "", "image": "bg20.png", "main_color": "#cc0000", "dark_color": "#7a0000"},
        {"sport": "default", "competition": "", "image": "bg01.png", "main_color": "#223047", "dark_color": "#141d2b"}
    ]

    event_lower = params["event_type"].lower()

    chosen = None
    for bg in backgrounds:
        if bg["sport"] in event_lower and (not bg["competition"] or bg["competition"] in event_lower):
            chosen = bg
            break

    if not chosen:
        chosen = backgrounds[-1]  # default

    try:
        bg_path = os.path.join("background", chosen["image"])
        with open(bg_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            mime = "image/jpeg" if chosen["image"].endswith((".jpg", ".jpeg")) else "image/png"
            chosen["image"] = f"data:{mime};base64,{b64}"
            print(f"✅ Background: {chosen['sport']} - {bg_path}")
    except FileNotFoundError:
        print(f"⚠️ File {chosen['image']} non trovato, sfondo disabilitato")
        chosen["image"] = None

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
