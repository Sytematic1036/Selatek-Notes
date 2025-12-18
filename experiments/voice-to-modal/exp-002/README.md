# exp-002: Session-baserad textackumulering

## Status: PLANNED

## Hypothesis
Modal Volume + session ID kan behålla state mellan dikteringar, och exportera till Word.

## Mål
1. Diktera text som visas direkt (utan JSON/status)
2. Fortsätt diktera - texten byggs på
3. Tryck "Spara till Word" för att exportera

## Teknisk approach

### State-lösning
- **Modal Volume:** Persistent fil-lagring
- **Session ID:** UUID genererat i iPhone Shortcut
- **Fil:** `/sessions/{session_id}.txt`

### Endpoints

| Endpoint | Metod | Beskrivning |
|----------|-------|-------------|
| `/accumulate` | POST | Lägg till text, returnera all ackumulerad text |
| `/save_to_word` | POST | Exportera till Word, rensa session |

### iPhone Shortcut-flöde
```
1. Generera UUID (session_id)
2. LOOP:
   - Diktera text
   - POST /accumulate med {session_id, text}
   - Visa texten (plain text, ej JSON)
   - Fråga: "Fortsätt?" eller "Spara till Word"
3. Om "Spara till Word":
   - POST /save_to_word med {session_id}
   - Ladda ner Word-fil
```

## Deploy

```bash
cd Selatek_Notes/experiments/voice-to-modal/exp-002
PYTHONUTF8=1 modal deploy app.py
```

## Test med curl

### Skapa session och lägg till text
```bash
# Första dikteringen
curl -X POST https://mackanh1972--voice-accumulator-accumulate.modal.run \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-123", "text": "Detta är första meningen."}'

# Andra dikteringen
curl -X POST https://mackanh1972--voice-accumulator-accumulate.modal.run \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-123", "text": "Detta är andra meningen."}'
```

### Spara till Word
```bash
curl -X POST https://mackanh1972--voice-accumulator-save-to-word.modal.run \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-123"}' \
  --output dikterad_text.docx
```

## Success Criteria
- [ ] Flera dikteringar ackumuleras korrekt
- [ ] Endast text visas (ingen JSON)
- [ ] Word-export fungerar
- [ ] Session rensas efter export
