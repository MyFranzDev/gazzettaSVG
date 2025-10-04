#!/usr/bin/env python3
"""
Generate text variants using OpenAI API
Usage: python3 generate_texts.py "Event description"
"""

import sys
import json
import os
from openai import OpenAI

def generate_text_variants(event_type):
    """Generate 3 text variants using OpenAI"""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    client = OpenAI(api_key=api_key)

    prompt = f"""
Sei un copywriter per La Gazzetta dello Sport.
Evento: {event_type}

Genera 3 varianti di copy per un banner promozionale:

1. FOMO (urgenza, occasione limitata)
2. Esclusiva (premium, riservata)
3. Soft (amichevole, inclusiva)

Per ogni variante genera:
- header (breve, 3-5 parole)
- main_title (accattivante, 6-10 parole)
- subtitle (dettaglio, 6-10 parole)
- cta (call to action, massimo 4 parole)

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
    return variants

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No event provided"}), file=sys.stderr)
        sys.exit(1)

    event_type = sys.argv[1]

    try:
        variants = generate_text_variants(event_type)
        # Output only JSON to stdout
        print(json.dumps(variants))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
