# exp-003: PWA med offline-stöd

## Status: PLANNED

## Hypothesis
En PWA (Progressive Web App) kan ge bättre användarupplevelse än iPhone Shortcuts, med offline-stöd och enkel distribution.

## Funktioner

- **Diktera** - Web Speech API (svenska)
- **Offline-stöd** - Text sparas lokalt i localStorage
- **Synka** - Skicka till Modal när online
- **Spara till Word** - Ladda ner .docx fil
- **Installera** - Lägg till på hemskärmen som app

## Filer

| Fil | Beskrivning |
|-----|-------------|
| index.html | Huvudsida med all kod |
| manifest.json | PWA-manifest för installation |
| sw.js | Service Worker för offline |

## Deploy

### Alternativ 1: Modal Static Files
```bash
# Lägg till static site serving i Modal
```

### Alternativ 2: GitHub Pages
```bash
# Pusha till GitHub och aktivera Pages
```

### Alternativ 3: Netlify/Vercel
```bash
# Deploya direkt från mappen
```

## Test lokalt

```bash
cd exp-003
python -m http.server 8000
# Öppna http://localhost:8000
```

## Installation på iPhone

1. Öppna URL i Safari
2. Tryck på "Dela" (fyrkant med pil upp)
3. Välj "Lägg till på hemskärmen"
4. Klart!

## Begränsningar

- Web Speech API kräver internet för diktering
- Word-export kräver internet
- Text sparas lokalt och synkas när online

## Success Criteria

- [ ] PWA installeras på iPhone
- [ ] Diktering fungerar (Web Speech API)
- [ ] Text sparas lokalt (offline)
- [ ] Synka till Modal fungerar
- [ ] Word-export fungerar
