# exp-001: Modal + iPhone Voice Input

## Status: COMPLETED

**Endpoint:** `https://mackanh1972--voice-receiver-receive-voice.modal.run`

## Hypothesis
Modal.com kan ta emot text via HTTP POST från iPhone Shortcuts, där texten kommer från iPhones inbyggda tal-till-text.

## Resultat: SUCCESS

---

## Steg

### 1. Deploya till Modal
```bash
cd Selatek_Notes/experiments/voice-to-modal/exp-001
PYTHONUTF8=1 modal deploy app.py
```
**OBS:** `PYTHONUTF8=1` krävs på Windows pga Unicode-tecken i Modal CLI output.

### 2. Testa med curl
```bash
curl -X POST https://mackanh1972--voice-receiver-receive-voice.modal.run \
  -H "Content-Type: application/json" \
  -d '{"text": "Hej från test"}'
```

Svar: `{"status":"success","received":"Hej från test","length":14,"message":"Mottog 14 tecken"}`

---

### 3. iPhone Shortcut (Svenska)

#### Action 1: Diktera text
- Sök efter **"Diktera"**
- Lägg till **"Diktera text"**

#### Action 2: Hämta innehåll från URL
- Sök efter **"Hämta innehåll"**
- Lägg till **"Hämta innehåll från URL"**
- Konfigurera:
  - **URL:** `https://mackanh1972--voice-receiver-receive-voice.modal.run`
  - **Metod:** POST
  - **Sidhuvuden:**
    - Nyckel: `Content-Type`
    - Värde: `application/json`
  - **Text i begäran:** JSON
    - **Nyckel:** `text`
    - **Värde:** Välj variabeln **Dikterad text** (blå bubbla)

#### Action 3: Visa
- Sök efter **"Visa"**
- Lägg till **"Visa"**
- Välj **"Innehåll i URL"** som värde
- **Fördel:** Resultatet stannar kvar på skärmen tills du trycker "Klar"

---

## Lärdomar

1. **Windows-fix:** `PYTHONUTF8=1` före `modal deploy`
2. **Rätt åtgärd:** "Hämta innehåll från URL" (INTE "URL" eller "URL-kodning")
3. **Visa resultat:** "Visa" + "Innehåll i URL" är bäst - stannar på skärmen
4. **Viktigt:** Nyckel-fältet (`text`) måste vara ifyllt i JSON body

---

## Success Criteria
- [x] Modal endpoint returnerar 200 på POST
- [x] iPhone Shortcut kan skicka text till endpoint
- [x] Bekräftelse visas på iPhone efter lyckad POST
