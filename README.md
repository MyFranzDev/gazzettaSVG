# Gazzetta Multi-Banner SVG Generator

Generatore automatico di banner SVG promozionali per Gazzetta dello Sport con integrazione AI e **architettura template-driven** per generazione multi-formato.

## 🎯 Caratteristiche

- **🚀 Multi-Banner Generation**: 1 input → N banner in formati diversi
- **📐 Template-Driven Architecture**: Layout definiti in JSON, zero duplicazione codice
- **🌐 Web Interface**: Frontend PHP intuitivo con wizard 5-step
- **✏️ Post-Generation Editing**: Modifica testi inline dopo la generazione con anteprima live
- **🤖 AI-Powered Copywriting**: Generazione automatica di 3 varianti di testi (FOMO, Esclusiva, Soft) tramite OpenAI
- **🎨 Auto Background Selection**: Selezione automatica dello sfondo in base a sport e competizione
- **🔤 Font Embedded**: Font Oswald e Roboto (Regular/Bold/Italic) incorporati nel SVG
- **💰 Split Price Display**: Prezzo separato da periodicità con layout complesso (integer grande + decimali piccoli)
- **🎨 Advanced Text Auto-sizing**: Algoritmo intelligente per riempire lo spazio disponibile
- **🖼️ Custom Logo Support**: Carica loghi personalizzati (versione full e small, white/dark backgrounds)
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

### Interfaccia Web (CONSIGLIATO) 🌐

L'applicazione include un'interfaccia web completa con wizard interattivo a 5 step.

#### Avvio Locale

```bash
cd web/frontend
php -S localhost:8000
```

Apri il browser su `http://localhost:8000` e accedi con password: `touchlabs2`

#### Wizard 5-Step

**Step 1: Evento e Sport**
- Inserisci nome evento
- **Prezzo separato**: Campo dedicato per prezzo (es. `0,99€`) e periodicità (es. `/mese`)
- Seleziona stile grafico (2 varianti con preview visiva)
- Scegli lo sport dalla griglia con emoji
- **Selezione sfondo dinamica**: Gli sfondi cambiano automaticamente in base allo sport selezionato

**Step 2: Risorse**
- **Logo personalizzati**: Carica loghi full e small per sfondi chiari/scuri (4 varianti)
- Logo Gazzetta precaricato (bianco/nero) come fallback
- Visualizza font disponibili (Oswald Bold/BoldItalic, Roboto Bold/BoldItalic/Regular)
- Carica immagine opzionale

**Step 3: Testi**
- Visualizza 3 varianti AI-generated per ogni campo (header, titolo, sottotitolo, CTA)
- Oppure scrivi testo personalizzato
- Associa font specifico per ogni campo

**Step 4: Genera**
- Seleziona formati banner da generare
- Checkbox multipli con "Seleziona tutti"
- Anteprima count banner selezionati
- **Loader animato** durante la generazione e conversione PNG

**Step 5: Download & Editing**
- Riepilogo configurazione
- **Preview PNG ad alta qualità** (generata con Puppeteer)
- **Modifica testi direttamente**: Header, Titolo, CTA, Prezzo, Periodicità
- **Rigenera singolo banner** con nuovi testi via AJAX
- **Notifiche animate** per feedback utente
- Download PNG (non modificabile dall'utente, SVG mantenuto server-side)

#### Caratteristiche Web Interface

- ✅ Session-based navigation con progress bar cliccabile
- ✅ Validazione step-by-step (bottoni disabilitati fino a completamento)
- ✅ Design responsive con tema Gazzetta (navy blue + gold)
- ✅ Snackbar notifications per funzioni demo
- ✅ Mock data per sviluppo frontend standalone
- ✅ **Post-generation editing**: Modifica inline con rigenerazione AJAX
- ✅ **API REST**: Endpoint `/api/regenerate_banner.php` per rigenerazione singoli banner
- ✅ **Notifiche animate**: Feedback visivo per operazioni utente
- ✅ **PNG ad alta qualità**: Conversione SVG→PNG con Puppeteer (headless Chrome) a 2x scale
- ✅ **Loader animato**: Overlay con spinner durante generazione e conversione
- ✅ **Sfondi sport-specific**: Selezione dinamica sfondi contestuale allo sport nello Step 1

---

### CLI - Generazione Multi-Banner

Per uso da linea di comando:

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
  12. 1200x1200
  13. 1920x1080
  14. TUTTI

Scegli template [1-14] o numeri separati da virgola (es. 1,3,5): 14
```

Opzioni:
- Singolo template: `3` → genera solo 300x250
- Multi selezione: `1,3,5,10` → genera 4 banner
- Tutti: `14` o `tutti` → genera tutti i formati

#### **STEP 6: Rendering Multi-Banner**
```
🚀 Generazione 13 banner in corso...
✅ Generated: output/184x90.svg
✅ Generated: output/285x130.svg
✅ Generated: output/300x250.svg
...
✅ Generated: output/1200x1200.svg
✅ Generated: output/1920x1080.svg
✅ Completato! 13 banner generati in 'output/'
```

## 📁 Struttura Progetto

```
.
├── gazzetta_multi_generator.py  # Script principale multi-banner (CLI)
├── template_engine.py           # Motore rendering generico
├── generate_single_banner.py    # Script per generazione singolo banner da JSON
├── svg_to_png.js                # Conversione SVG→PNG con Puppeteer
├── web/                         # Applicazione web
│   └── frontend/                # Frontend PHP
│       ├── index.php            # Login page
│       ├── wizard.php           # Wizard principale (5 step)
│       ├── logout.php           # Logout handler
│       ├── styles.css           # Stili Gazzetta theme
│       ├── script.js            # Utility JavaScript
│       ├── steps/               # Step wizard
│       │   ├── step1.php        # Evento, sport e sfondi
│       │   ├── step2.php        # Risorse (loghi, font, immagini)
│       │   ├── step3.php        # Testi AI
│       │   ├── step4.php        # Selezione formati e generazione
│       │   └── step5.php        # Preview, editing e download
│       ├── api/                 # API endpoints
│       │   └── regenerate_banner.php  # Rigenerazione singolo banner
│       ├── backgrounds/         # 47+ sfondi PNG
│       ├── logos/               # Loghi Gazzetta (bianco/nero, full/small)
│       ├── generated/           # Banner generati (SVG + PNG)
│       └── fonts/               # Font woff2
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
│   ├── 735x280.json             # Large billboard
│   ├── 1200x1200.json           # Square Social Media
│   └── 1920x1080.json           # Full HD Landscape
├── font/                        # Font embedded per CLI
│   ├── Oswald-Bold.woff2
│   ├── Roboto-Regular.woff2
│   └── Roboto-Bold.woff2
├── background/                  # Sfondi disponibili
│   ├── bg01.png - bg47.png      # 47+ sfondi organizzati per sport
├── images/                      # Immagini da usare nei banner
│   └── calcio.jpg
└── output/                      # Banner generati (CLI)
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
| Leaderboard | 728x90 | Horizontal | Logo, Titolo, CTA compatto |
| Large Billboard | 735x280 | Horizontal | Logo, Titolo, Subtitle, CTA |
| Square Social | 1200x1200 | Square | Logo+Header, Titolo, Smartphone, Descrizione, Prezzo, CTA, Logo Footer |
| Full HD Landscape | 1920x1080 | Landscape | Logo+Header, Area centrale bianca, Colonne laterali simmetriche |

### Tipi di Componenti Supportati

Il template engine supporta 11 tipi di componenti:

1. **`background_layer`** - Layer di sfondo colorato o immagine con clipping
2. **`text_block`** - Blocco testo con header e title auto-sized (40/60 split)
3. **`text_only`** - Solo testo senza sfondo, con auto-sizing opzionale e alignment (left/right/center)
4. **`image`** - Immagine utente semplice
5. **`smartphone_mockup`** - Mockup smartphone con immagine e badge
6. **`cta_button`** - Pulsante call-to-action con auto-sizing e italic support
7. **`logo`** - Logo personalizzato o G+ Gazzetta (supporta upload utente)
8. **`bullet_list`** - Lista puntata con checkmark
9. **`price_display`** - Display prezzo complesso con alignment dinamico (left/right/center)
10. **`logo_text_group`** - Logo + testo auto-centrati orizzontalmente con color filter support

## 🎯 Sfondi Supportati per Sport

Gli sfondi sono organizzati per sport e vengono mostrati dinamicamente nello Step 1 quando si seleziona uno sport.

### Generico (22 sfondi)
bg01, bg02, bg03, bg06, bg08, bg09, bg10, bg11, bg12, bg13, bg19, bg20, bg25, bg27, bg34, bg35, bg36, bg37, bg38, bg39, bg40, bg41

### Calcio (21 sfondi)
- Champions League: bg15, bg16, bg17
- Calcio: bg18, bg19, bg20, bg22, bg23, bg24, bg30, bg31, bg32, bg33, bg34, bg35, bg36, bg37, bg38, bg39, bg40, bg41

### Tennis (8 sfondi)
bg09, bg10, bg11 (Wimbledon), bg12 (US Open), bg42, bg43, bg44, bg45 (Australian Open)

### Pallavolo/Volley (7 sfondi)
bg06, bg07, bg08, bg09, bg10, bg46, bg47

### Ciclismo (1 sfondo)
bg14

### Golf (2 sfondi)
bg19, bg20

### Formula 1/Moto GP (5 sfondi)
bg25, bg26, bg27, bg28, bg29

## 🎨 Template 1920x1080 "Full HD Banner"

Il nuovo template Full HD 1920x1080 è un banner orizzontale premium con layout simmetrico e funzionalità avanzate.

### Caratteristiche Principali

- **Top overlay semitrasparente**: Fascia superiore 1920x140px con overlay rgba(10, 20, 40, 0.65)
- **Bottom overlay semitrasparente**: Fascia inferiore 1920x125px con stesso overlay, sotto la parte bianca
- **Centro bianco**: Area centrale 977x970px (x=471, y=110) che si sovrappone 30px alla fascia superiore
- **Logo+Text auto-centered**: Nuovo componente `logo_text_group` con:
  - Auto-centering orizzontale del gruppo logo+testo
  - Calcolo dinamico larghezza testo (char_width_ratio 0.55 per Oswald, 0.6 per altri)
  - Color filter SVG per colorare il logo (#bb2b60)
  - Vertical adjustment (-10px per spostare in alto)
- **Colonne laterali simmetriche**: 150px di larghezza con 12px padding verso centro
  - **Left column** (x=321): elementi allineati a destra
  - **Right column** (x=1460): elementi allineati a sinistra
  - Contenuto: smartphone 80x145px, description, price, CTA 130x40px
- **Price display con alignment dinamico**:
  - **Right alignment**: parte decimale allineata a destra, intero a sinistra
  - **Left alignment**: parte intera allineata a sinistra, decimale a destra
  - Calcolo dinamico larghezze per posizionamento
- **Text alignment avanzato**: Supporto completo per left/right/center con SVG text-anchor
- **Debug guides opzionale**: Barre rosse/verdi 12px per verificare padding (disabilitabili con `debug_guides: false`)

### Layout (1920x1080px)

```
┌─────────────────────────────────────────────────────────────┐
│  TOP OVERLAY (140px) - rgba(10,20,40,0.65)                  │
│     [Logo Rosa] HEADER: TITLE                               │
├──────┬────────────────────────────────────────────┬─────────┤
│ LEFT │      CENTER WHITE AREA (977x970)           │  RIGHT  │
│ COL  │                                            │   COL   │
│150px │         (Content goes here)                │  150px  │
│      │                                            │         │
│ 📱   │                                            │    📱   │
│ Desc │                                            │   Desc  │
│Price │                                            │  Price  │
│ CTA  │                                            │   CTA   │
├──────┴────────────────────────────────────────────┴─────────┤
│  BOTTOM OVERLAY (125px) - rgba(10,20,40,0.65)               │
└─────────────────────────────────────────────────────────────┘
```

### Spacing e Allineamento

- **Top overlay**: y=0, height=140px
- **White area**: y=110, height=970px (overlap 30px con top)
- **Bottom overlay**: y=955, height=125px (sotto white area)
- **Side columns padding**: 12px verso centro
- **Elements vertical spacing**: smartphone→description: 15px, description→price: 40px, price→CTA: 15px
- **Elements vertical alignment**: tutti allineati verso l'alto a y=140

### Esempio Template JSON

```json
{
  "id": "top_logo_text",
  "type": "logo_text_group",
  "logo_source": "logo_small_dark",
  "text_source": "header_title_combined",
  "geometry": {"x": 0, "y": 0, "width": 1920, "height": 140},
  "style": {
    "text_color": "#FFFFFF",
    "font_family": "Oswald Bold",
    "font_style": "italic",
    "font_size": 48,
    "logo_size": 100,
    "logo_padding": 8,
    "gap": 10,
    "logo_color": "#bb2b60"
  }
}
```

### Color Filter per Logo

Il componente `logo_text_group` supporta `logo_color` per colorare dinamicamente il logo tramite SVG `feColorMatrix`:

```python
# Converte hex #bb2b60 in valori RGB normalizzati
R = int("bb", 16) / 255  # 0.733
G = int("2b", 16) / 255  # 0.169
B = int("60", 16) / 255  # 0.376
```

---

## 🎨 Template 728x90 "Bologna Style"

Il template Leaderboard 728x90 è stato completamente ridisegnato con funzionalità avanzate:

### Caratteristiche Principali

- **Background full-width con overlay**: Immagine di sfondo a piena larghezza con overlay semi-trasparente (65% opacità) sul lato sinistro
- **Logo personalizzato small**: Supporto per logo utente in versione compatta (95x90px)
- **Text block auto-sized**: Header e title con auto-sizing intelligente (split 40/60)
- **Price display complesso**:
  - Numero intero grande (75% altezza)
  - Decimali piccoli top-right (35% altezza)
  - Periodicità piccola bottom-right (25% altezza)
  - Spacing di 5px tra componenti
  - Supporto font italic
- **CTA button**: Auto-sizing con border-radius ridotto (8px) e italic support
- **Vertical centering**: Tutti i testi centrati verticalmente nello spazio disponibile

### Layout (728x90px)

```
[Logo 95px] [Header + Title 270px] [Price 165px] [CTA 155px]
                                    14  ,99€
                                        /ANNO
```

### Esempio Template JSON

```json
{
  "id": "price_block",
  "type": "price_display",
  "price_source": "price",
  "period_source": "price_period",
  "geometry": {"x": 383, "y": 0, "width": 165, "height": 90},
  "style": {
    "text_color": "#FFFFFF",
    "font_family": "Oswald Bold",
    "font_style": "italic",
    "alignment": "center"
  }
}
```

### Font Support

Il template supporta font italic:
- **Oswald Bold Italic** (o fallback Oswald HeavyItalic 800 TTF)
- **Roboto Bold Italic**

Entrambi embedding via WOFF2 o TTF, con auto-fallback a system fonts.

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
