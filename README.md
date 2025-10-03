# Gazzetta SVG Banner Generator

Generatore automatico di banner SVG promozionali per Gazzetta dello Sport con integrazione AI.

## 🎯 Caratteristiche

- **6 Step Workflow**: Processo procedurale chiaro e debuggabile
- **AI-Powered Copywriting**: Generazione automatica di 3 varianti di testi (FOMO, Esclusiva, Soft) tramite OpenAI
- **Auto Background Selection**: Selezione automatica dello sfondo in base a sport e competizione
- **Font Embedded**: Font Oswald e Roboto incorporati nel SVG (nessuna dipendenza esterna)
- **Customizzabile**: Template, colori, dimensioni e layout completamente configurabili
- **Output SVG**: File vettoriale scalabile e leggero

## 📋 Prerequisiti

- Python 3.7+
- OpenAI API Key
- Struttura cartelle:
  - `font/` - Font files (Oswald-Bold.woff2, Roboto-Regular.woff2, Roboto-Bold.woff2)
  - `background/` - Immagini di sfondo (bg01.png, bg15.png, ecc.)
  - `images/` - Immagini da inserire nei banner

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

### Esecuzione Base

```bash
python gazzetta_svg_generator.py
```

### Workflow Interattivo

Lo script ti guiderà attraverso 6 step:

#### **STEP 1: Parametri Banner**
```
Evento [Calcio - Finale Champions League]: Tennis - Wimbledon
Prezzo [14,99€ / ANNO]: 9,99€ / MESE
Larghezza [600]: 800
Altezza [500]: 600
```

#### **STEP 2: Generazione Testi**
L'AI genera automaticamente 3 varianti di testi:
- **FOMO**: Urgenza, occasione limitata
- **Esclusiva**: Premium, riservata
- **Soft**: Amichevole, inclusiva

#### **STEP 3: Selezione Template e Testi**
Scegli quale variante usare per ogni elemento:
```
Scegli la variante per ogni elemento:
Header [1-3, default=1]: 1
Main Title [1-3, default=1]: 2
Subtitle [1-3, default=1]: 1
CTA [1-3, default=1]: 3
```

Opzionalmente carica un'immagine:
```
Path immagine opzionale (invio per saltare): /path/to/image.png
Mostra immagine dentro smartphone? (s/n, default=n): n
```

#### **STEP 4: Selezione Sfondo**
Il sistema seleziona automaticamente lo sfondo appropriato in base a:
- **Sport**: calcio, tennis, volley
- **Competition**: champions league, serie a, wimbledon, roland garros, us open, ecc.

#### **STEP 5: Assemblaggio Template**
Tutti i componenti vengono assemblati in un template JSON finale.

#### **STEP 6: Rendering SVG**
Il banner viene generato come file SVG: `banner.svg`

## 📁 Struttura Progetto

```
.
├── gazzetta_svg_generator.py   # Script principale
├── font/                        # Font embedded
│   ├── Oswald-Bold.woff2
│   ├── Roboto-Regular.woff2
│   └── Roboto-Bold.woff2
├── background/                  # Sfondi disponibili
│   ├── bg01.png
│   ├── bg15.png (Champions League)
│   └── ...
├── images/                      # Immagini da usare nei banner
│   └── calcio.jpg
└── banner.svg                   # Output generato
```

## 🎨 Template Disponibili

### Template 1 (Default)
- **Header**: 20% altezza, colore dinamico basato su sfondo
- **Main Title**: 10% altezza, centrato
- **Body**:
  - Left (40%): Spazio per immagine opzionale
  - Right (60%): Subtitle + Prezzo + CTA
- **Footer**: 10% altezza, branding Gazzetta

## 🎯 Sfondi Supportati

### Calcio
- Champions League (blu UEFA)
- Serie A (azzurro)
- Coppa Italia (verde)

### Tennis
- Wimbledon (verde)
- Roland Garros (rosso terra)
- US Open (giallo)

### Volley
- Pallavolo generica (rosso)

### Default
- Sfondi neutri per sport non riconosciuti

## 🔧 Configurazione Avanzata

### Modifica Template

Puoi modificare il template base in `step3_select_template_and_texts()`:

```python
template_base = {
    "width": 500,
    "height": 500,
    "header": {
        "background": "#223047",  # Colore header
        "color": "#FFFFFF",       # Colore testo
        "height_ratio": 0.2       # 20% altezza
    },
    # ... altri parametri
}
```

### Aggiungere Nuovi Sfondi

Modifica l'array `backgrounds` in `step4_pick_background()`:

```python
backgrounds = [
    {
        "sport": "basket",
        "competition": "nba",
        "image": "bg_nba.png",
        "main_color": "#17408B",
        "dark_color": "#0B1F45"
    },
    # ... altri sfondi
]
```

### Personalizzare Prompt AI

Modifica il prompt in `step2_generate_texts()` per cambiare il tone of voice:

```python
prompt = f"""
Sei un copywriter per [TUO BRAND].
Evento: {event_type}

Genera testi con stile [TUO STILE]...
"""
```

## 🐛 Debug

Lo script è organizzato in step procedurali per facilitare il debug:

```python
# Ogni step è una funzione indipendente
step1_get_parameters()      # Raccolta parametri
step2_generate_texts()      # AI text generation
step3_select_template()     # Selezione template
step4_pick_background()     # Background matching
step5_build_template()      # Template assembly
step6_render_svg()          # SVG rendering
```

Puoi commentare/testare singoli step o aggiungere `print()` per ispezionare i dati.

## 📝 Esempio Output

```svg
<svg width="600" height="500" ...>
  <!-- Header con testo generato da AI -->
  <!-- Main title dell'evento -->
  <!-- Background automatico basato su sport -->
  <!-- Immagine opzionale -->
  <!-- Subtitle + Prezzo + CTA -->
  <!-- Footer branding -->
</svg>
```

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

## 🤝 Contributing

Contributi, issues e feature requests sono benvenuti!

## 📄 Licenza

Questo progetto è stato sviluppato per uso interno di Gazzetta dello Sport.

## 🙏 Credits

- **AI**: OpenAI GPT-4 per la generazione dei copy
- **Fonts**: Google Fonts (Oswald, Roboto)
- **Sviluppo**: Convertito da Jupyter Notebook con Claude Code

---

**Nota**: Ricorda di non committare mai la tua API key nel repository. Usa sempre variabili d'ambiente!
