# Gazzetta Multi-Banner SVG Generator

Generatore automatico di banner SVG promozionali per Gazzetta dello Sport con integrazione AI e **architettura template-driven** per generazione multi-formato.

## 🎯 Caratteristiche

- **🚀 Multi-Banner Generation**: 1 input → N banner in formati diversi
- **📐 Template-Driven Architecture**: Layout definiti in JSON, zero duplicazione codice
- **🤖 AI-Powered Copywriting**: Generazione automatica di 3 varianti di testi (FOMO, Esclusiva, Soft) tramite OpenAI
- **🎨 Auto Background Selection**: Selezione automatica dello sfondo in base a sport e competizione
- **🔤 Font Embedded**: Font Oswald e Roboto incorporati nel SVG (nessuna dipendenza esterna)
- **⚡ Scalabile**: Aggiungi nuovi template senza modificare codice Python
- **📦 Output SVG**: File vettoriali scalabili e leggeri

## 📋 Prerequisiti

- Python 3.7+
- OpenAI API Key
- Struttura cartelle:
  - `font/` - Font files (Oswald-Bold.woff2, Roboto-Regular.woff2, Roboto-Bold.woff2)
  - `background/` - Immagini di sfondo (bg01.png, bg15.png, ecc.)
  - `images/` - Immagini da inserire nei banner
  - `templates/` - Template JSON per i diversi formati

## 🚀 Installazione

```bash
# Clone del repository
git clone https://github.com/MyFranzDev/gazzettaSVG.git
cd gazzettaSVG

# Installazione dipendenze
pip install openai

# Configurazione API Key
export OPENAI_API_KEY='your-openai-api-key-here'
```

## 💻 Utilizzo

### Generazione Multi-Banner (CONSIGLIATO)

```bash
python gazzetta_multi_generator.py
```

### Workflow Interattivo

Lo script ti guiderà attraverso 6 step:

#### **STEP 1: Parametri Evento e Sport**
```
Evento [Tennis - US Open]: Calcio - Champions League
Prezzo [0,99€ / mese]: 14,99€ / anno

Sport:
  1. Calcio
  2. Tennis
  3. Pallavolo/Volley
  4. Ciclismo
  5. Golf
  6. Formula 1/Moto GP
  7. Generico
  8. Altro (scrivi manualmente)

Scegli sport [1-8]: 1
✅ Sport selezionato: Calcio
```

#### **STEP 2: Generazione Testi AI**
L'AI genera automaticamente 3 varianti di testi:
- **FOMO**: Urgenza, occasione limitata
- **Esclusiva**: Premium, riservata
- **Soft**: Amichevole, inclusiva

Esempio output:
```
VARIANT_1_FOMO:
  header: Solo per poco!
  main_title: L'US Open ti aspetta!
  subtitle: Non perdere l'evento sportivo dell'anno
  cta: Agisci ora

VARIANT_2_ESCLUSIVA:
  header: Accesso Premium
  main_title: US Open come mai prima
  subtitle: Goditi l'esperienza esclusiva riservata
  cta: Accedi Ora

VARIANT_3_SOFT:
  header: Ama il Tennis?
  main_title: Unisciti a noi all'US Open
  subtitle: Condividi l'emozione del grande tennis
  cta: Partecipa subito
```

#### **STEP 3: Selezione Testi**
Scegli quale variante usare per ogni elemento:
```
HEADER:
  1. Solo per poco!
  2. Accesso Premium
  3. Ama il Tennis?
Scegli [1, 2, 3] (default=1): 2
```

#### **STEP 4: Caricamento Risorse**
```
Path immagine opzionale (invio per saltare): images/calcio.jpg
✅ Immagine caricata: images/calcio.jpg

🎨 Selezione background...

Background disponibili per Calcio:
  1. bg15.png - Champions League 1
  2. bg16.png - Champions League 2
  3. bg17.png - Champions League 3
  4. bg18.png - Generico 1
  5. bg19.png - Generico 2
  6. bg20.png - Generico 3
  7. bg22.png - Generico 4
  8. bg23.png - Generico 5
  9. bg24.png - Generico 6

Scegli background [1-9] (default=1): 2
✅ Background: bg16.png (Champions League 2)
```

Il sistema mostra gli sfondi disponibili per lo sport selezionato nello Step 1, permettendo di scegliere quello più appropriato al contesto.

#### **STEP 5: Selezione Template**
```
Template disponibili:
  1. 184x90
  2. 285x130
  3. 300x250
  4. 300x480
  5. 300x600
  6. 308x313
  7. 309x338
  8. 320x50
  9. 350x250
  10. 728x90
  11. 735x280
  12. TUTTI

Scegli template [1-12] o numeri separati da virgola (es. 1,3,5): 12
```

Opzioni:
- Singolo template: `3` → genera solo 300x250
- Multi selezione: `1,3,5,10` → genera 4 banner
- Tutti: `12` o `tutti` → genera tutti i formati

#### **STEP 6: Rendering Multi-Banner**
```
🚀 Generazione 11 banner in corso...
✅ Generated: output/184x90.svg
✅ Generated: output/285x130.svg
✅ Generated: output/300x250.svg
...
✅ Completato! 11 banner generati in 'output/'
```

## 📁 Struttura Progetto

```
.
├── gazzetta_multi_generator.py  # Script principale multi-banner
├── template_engine.py           # Motore rendering generico
├── gazzetta_svg_generator.py    # Script legacy (singolo banner)
├── templates/                   # Template JSON
│   ├── 184x90.json              # Small banner
│   ├── 285x130.json             # Medium banner
│   ├── 300x250.json             # Medium rectangle
│   ├── 300x480.json             # Vertical
│   ├── 300x600.json             # Half page
│   ├── 308x313.json             # Square
│   ├── 309x338.json             # Square
│   ├── 320x50.json              # Mobile banner
│   ├── 350x250.json             # Medium
│   ├── 728x90.json              # Leaderboard
│   └── 735x280.json             # Large billboard
├── font/                        # Font embedded
│   ├── Oswald-Bold.woff2
│   ├── Roboto-Regular.woff2
│   └── Roboto-Bold.woff2
├── background/                  # Sfondi disponibili
│   ├── bg01.png
│   ├── bg15.png (Champions League)
│   ├── bg19.png (US Open)
│   └── ...
├── images/                      # Immagini da usare nei banner
│   └── calcio.jpg
└── output/                      # Banner generati
    ├── 184x90.svg
    ├── 300x250.svg
    └── ...
```

## 🎨 Template Disponibili

### Formati Standard Pubblicitari

| Formato | Dimensioni | Tipo | Componenti |
|---------|-----------|------|------------|
| Mobile Banner | 320x50 | Horizontal | Logo, Titolo, CTA |
| Small Banner | 184x90 | Horizontal | Smartphone mini, CTA |
| Medium Banner | 285x130 | Horizontal | Smartphone, Titolo, Subtitle, CTA |
| Medium Rectangle | 300x250 | Square | Smartphone, Titolo, Subtitle, CTA |
| Square | 308x313 | Square | Smartphone, Titolo, Subtitle, Bullets, CTA |
| Square | 309x338 | Square | Smartphone, Titolo, Subtitle, Bullets, CTA |
| Medium | 350x250 | Horizontal | Smartphone, Titolo, Subtitle, CTA |
| Vertical | 300x480 | Vertical | Titolo, Subtitle, Bullets, Smartphone, CTA |
| Half Page | 300x600 | Vertical | Titolo, Subtitle, Bullets, Smartphone, CTA |
| Leaderboard | 728x90 | Horizontal | Logo, Titolo, Subtitle, CTA |
| Large Billboard | 735x280 | Horizontal | 2 Smartphone, Titolo, Subtitle, Bullets, CTA |

### Tipi di Componenti Supportati

Il template engine supporta 9 tipi di componenti:

1. **`background_layer`** - Layer di sfondo colorato
2. **`text_block`** - Blocco testo con background
3. **`text_only`** - Solo testo senza sfondo
4. **`image`** - Immagine utente semplice
5. **`smartphone_mockup`** - Mockup smartphone con immagine e badge
6. **`cta_button`** - Pulsante call-to-action
7. **`logo`** - Logo G+ Gazzetta
8. **`bullet_list`** - Lista puntata con checkmark

## 🎯 Sfondi Supportati per Sport

### Generico
- Sfondo 1 - bg01.png
- Sfondo 2 - bg02.png
- Sfondo 3 - bg03.png

### Calcio
- Champions League 1 - bg15.png
- Champions League 2 - bg16.png
- Champions League 3 - bg17.png
- Generico 1 - bg18.png
- Generico 2 - bg19.png
- Generico 3 - bg20.png
- Generico 4 - bg22.png
- Generico 5 - bg23.png
- Generico 6 - bg24.png

### Tennis
- Wimbledon - bg11.png
- US Open - bg12.png

### Pallavolo/Volley
- Volley 1 - bg06.png
- Volley 2 - bg07.png
- Volley 3 - bg08.png
- Volley 4 - bg09.png
- Volley 5 - bg10.png

### Ciclismo
- Ciclismo - bg14.png

### Golf
- Golf 1 - bg21.png
- Golf 2 - bg13.png

### Formula 1/Moto GP
- F1/MotoGP 1 - bg25.png
- F1/MotoGP 2 - bg26.png
- F1/MotoGP 3 - bg27.png
- F1/MotoGP 4 - bg28.png
- F1/MotoGP 5 - bg29.png

## 🔧 Configurazione Avanzata

### Creare un Nuovo Template

Basta creare un file JSON nella cartella `templates/`:

```json
{
  "name": "Il Mio Banner 400x300",
  "width": 400,
  "height": 300,
  "components": [
    {
      "id": "background",
      "type": "background_layer",
      "geometry": {
        "x": 0,
        "y": 0,
        "width": "100%",
        "height": "100%"
      }
    },
    {
      "id": "logo",
      "type": "logo",
      "geometry": {
        "x": 10,
        "y": 10,
        "width": 60,
        "height": 60
      },
      "style": {
        "background": "#E4087C",
        "font_size": 24,
        "show_subtitle": true
      }
    },
    {
      "id": "title",
      "type": "text_only",
      "content_source": "main_title",
      "geometry": {
        "x": 80,
        "y": 20,
        "width": 310,
        "height": 50
      },
      "style": {
        "text_color": "#FFFFFF",
        "font_size": 24,
        "font_family": "Oswald Bold",
        "alignment": "left"
      }
    },
    {
      "id": "cta",
      "type": "cta_button",
      "content_source": "cta_text",
      "geometry": {
        "x": 80,
        "y": 250,
        "width": 310,
        "height": 40
      },
      "style": {
        "background": "#FFD700",
        "text_color": "#000000",
        "font_size": 16,
        "font_family": "Roboto Bold",
        "border_radius": 20
      }
    }
  ]
}
```

**Nessuna modifica al codice Python necessaria!** Il template sarà automaticamente disponibile nel menu di selezione.

### Geometria dei Componenti

Il sistema supporta:
- **Valori percentuali**: `"width": "50%"` → 50% del canvas
- **Valori pixel**: `"width": "200px"` o `"width": 200` → dimensione assoluta
- **Dimensioni auto**: `"width": "100%"` → larghezza piena

### Content Sources

I template possono accedere a questi dati dinamici:

- `header_text` - Header generato da AI
- `main_title` - Titolo principale
- `subtitle` - Sottotitolo
- `cta_text` - Call to action
- `user_image` - Immagine caricata dall'utente
- `bullet1`, `bullet2`, `bullet3` - Bullet points predefiniti

### Aggiungere Nuovi Sfondi

Modifica il dizionario `backgrounds_catalog` in `gazzetta_multi_generator.py` (step4):

```python
backgrounds_catalog = {
    "Basket": [
        {"name": "NBA", "file": "bg_nba.png", "color": "#17408B"},
        {"name": "Eurolega", "file": "bg_euroleague.png", "color": "#FF6600"}
    ],
    # ... altri sport
}
```

Non dimenticare di aggiungere lo sport anche nel menu dello Step 1:

```python
sports = [
    "Calcio",
    "Tennis",
    # ... altri sport
    "Basket",  # <-- aggiungi qui
    "Generico",
    "Altro (scrivi manualmente)"
]
```

### Personalizzare Prompt AI

Modifica il prompt in `step2_generate_texts()` per cambiare il tone of voice:

```python
prompt = f"""
Sei un copywriter per [TUO BRAND].
Evento: {params['event_type']}

Genera testi con stile [TUO STILE]...
"""
```

## 🐛 Debug

### Template Engine

Il motore di rendering (`template_engine.py`) è completamente modulare:

```python
from template_engine import TemplateEngine, load_template

# Inizializza engine
engine = TemplateEngine()
engine.load_fonts()

# Carica template
template = load_template("templates/300x250.json")

# Imposta dati
engine.set_content_data({
    "main_title": "Il mio titolo",
    "cta_text": "Iscriviti ora"
})

# Renderizza
svg = engine.render_template(template)
```

### Testing Singolo Template

Per testare un template specifico senza input interattivo:

```python
python3 -c "
from template_engine import *
import json

engine = TemplateEngine()
engine.load_fonts()

template = load_template('templates/300x250.json')
engine.set_content_data({'main_title': 'Test', 'cta_text': 'Click'})

svg = engine.render_template(template)
save_svg(svg, 'test.svg')
"
```

## 📊 Vantaggi Architettura Template-Driven

| Prima (Procedurale) | Ora (Template-Driven) |
|---------------------|----------------------|
| 1 script → 1 banner | 1 script → N banner |
| Layout hardcoded | Layout in JSON |
| 20 formati = duplicazione codice | 20 formati = 20 file JSON |
| Modifiche = toccare Python | Modifiche = modificare JSON |
| Solo dev può creare template | Designer può creare template |

## ⚠️ Troubleshooting

### Errore: Missing OPENAI_API_KEY
```bash
export OPENAI_API_KEY='your-key'
```

### Font non trovati
Lo script funziona anche senza font (usa font di sistema come fallback)

Per migliore qualità, scarica i font da [Google Fonts](https://fonts.google.com/) e inseriscili nella cartella `font/`:
- [Oswald](https://fonts.google.com/specimen/Oswald)
- [Roboto](https://fonts.google.com/specimen/Roboto)

### Sfondo non trovato
Assicurati che i file PNG degli sfondi siano nella cartella `background/`.

### Immagine non trovata
Le immagini da inserire nei banner vanno posizionate nella cartella `images/`.

### Template non riconosciuto
Verifica che:
- Il file JSON sia nella cartella `templates/`
- Il JSON sia valido (usa [jsonlint.com](https://jsonlint.com/) per validare)
- La struttura segua il formato corretto (vedi esempi sopra)

## 🚀 Roadmap

- [ ] Supporto per gradient background
- [ ] Animazioni SVG opzionali
- [ ] Export in PNG/JPG oltre a SVG
- [ ] UI web per creazione template
- [ ] Template marketplace

## 🤝 Contributing

Contributi, issues e feature requests sono benvenuti!

Per aggiungere un nuovo formato:
1. Crea il file JSON in `templates/`
2. Testa con `python gazzetta_multi_generator.py`
3. Apri una PR con il nuovo template

## 📄 Licenza

Questo progetto è stato sviluppato per uso interno di Gazzetta dello Sport.

## 🙏 Credits

- **AI**: OpenAI GPT-4 per la generazione dei copy
- **Fonts**: Google Fonts (Oswald, Roboto)
- **Architettura**: Template-driven design with Claude Code
- **Sviluppo**: Convertito da Jupyter Notebook e refactored con architettura scalabile

---

**Nota**: Ricorda di non committare mai la tua API key nel repository. Usa sempre variabili d'ambiente!
