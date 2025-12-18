"""
exp-003: PWA Static File Server med foto-stöd
Serves the PWA files from Modal
"""
import modal
from pathlib import Path

app = modal.App("selatek-notes-pwa")

image = modal.Image.debian_slim().pip_install("fastapi")

@app.function(image=image)
@modal.asgi_app()
def web():
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse, Response

    web_app = FastAPI()

    INDEX_HTML = '''<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Selatek Notes">
    <title>Selatek Notes</title>
    <link rel="manifest" href="manifest.json">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
            padding-top: env(safe-area-inset-top, 20px);
            padding-bottom: env(safe-area-inset-bottom, 20px);
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 24px;
        }

        .status {
            text-align: center;
            font-size: 12px;
            color: #888;
            margin-bottom: 20px;
        }

        .status.online { color: #4ade80; }
        .status.offline { color: #f87171; }

        .text-area {
            width: 100%;
            min-height: 250px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            padding: 15px;
            color: #fff;
            font-size: 16px;
            line-height: 1.6;
            resize: none;
            margin-bottom: 15px;
        }

        .text-area:focus {
            outline: none;
            border-color: #60a5fa;
        }

        .text-area::placeholder {
            color: rgba(255,255,255,0.4);
        }

        .image-preview {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }

        .image-preview img {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 8px;
            border: 2px solid rgba(255,255,255,0.3);
        }

        .image-preview .img-container {
            position: relative;
        }

        .image-preview .img-label {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.7);
            color: #fff;
            font-size: 10px;
            text-align: center;
            padding: 2px;
            border-radius: 0 0 6px 6px;
        }

        .buttons {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .btn-row {
            display: flex;
            gap: 10px;
        }

        .btn-row button {
            flex: 1;
        }

        button {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.1s, opacity 0.2s;
        }

        button:active {
            transform: scale(0.98);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-dictate {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: #fff;
        }

        .btn-dictate.recording {
            background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .btn-photo {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #fff;
        }

        .btn-save {
            background: linear-gradient(135deg, #10b981 0%, #047857 100%);
            color: #fff;
        }

        .btn-clear {
            background: rgba(255,255,255,0.1);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .word-count {
            text-align: center;
            font-size: 12px;
            color: #888;
            margin-top: 10px;
        }

        .toast {
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.8);
            color: #fff;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
        }

        .toast.show {
            opacity: 1;
        }

        #cameraInput {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Selatek Notes</h1>
        <div class="status" id="status">Kontrollerar anslutning...</div>

        <textarea
            class="text-area"
            id="textArea"
            placeholder="Tryck på mikrofonen för att diktera, eller skriv direkt här..."
        ></textarea>

        <div class="image-preview" id="imagePreview"></div>

        <div class="buttons">
            <div class="btn-row">
                <button class="btn-dictate" id="dictateBtn">
                    🎤 Diktera
                </button>
                <button class="btn-photo" id="photoBtn">
                    📷 Foto
                </button>
            </div>
            <button class="btn-save" id="saveBtn">
                💾 Spara till Word
            </button>
            <button class="btn-clear" id="clearBtn">
                🗑️ Rensa
            </button>
        </div>

        <div class="word-count" id="wordCount">0 tecken | 0 bilder</div>
    </div>

    <input type="file" id="cameraInput" accept="image/*" capture="environment">
    <div class="toast" id="toast"></div>

    <script>
        const API_URL = 'https://mackanh1972--voice-accumulator-accumulate.modal.run';
        const IMAGE_API_URL = 'https://mackanh1972--voice-accumulator-add-image.modal.run';
        const WORD_API_URL = 'https://mackanh1972--voice-accumulator-save-to-word.modal.run';
        const STORAGE_KEY = 'selatek-notes-text';
        const IMAGES_KEY = 'selatek-notes-images';
        const SESSION_KEY = 'selatek-notes-session';

        const textArea = document.getElementById('textArea');
        const dictateBtn = document.getElementById('dictateBtn');
        const photoBtn = document.getElementById('photoBtn');
        const saveBtn = document.getElementById('saveBtn');
        const clearBtn = document.getElementById('clearBtn');
        const statusEl = document.getElementById('status');
        const wordCountEl = document.getElementById('wordCount');
        const toast = document.getElementById('toast');
        const cameraInput = document.getElementById('cameraInput');
        const imagePreview = document.getElementById('imagePreview');

        let isRecording = false;
        let recognition = null;
        let images = [];

        function getSessionId() {
            let sessionId = localStorage.getItem(SESSION_KEY);
            if (!sessionId) {
                sessionId = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem(SESSION_KEY, sessionId);
            }
            return sessionId;
        }

        function saveLocal() {
            localStorage.setItem(STORAGE_KEY, textArea.value);
            localStorage.setItem(IMAGES_KEY, JSON.stringify(images));
            updateWordCount();
        }

        function loadLocal() {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                textArea.value = saved;
            }
            const savedImages = localStorage.getItem(IMAGES_KEY);
            if (savedImages) {
                images = JSON.parse(savedImages);
                renderImages();
            }
            updateWordCount();
        }

        function updateStatus() {
            if (navigator.onLine) {
                statusEl.textContent = '🟢 Online';
                statusEl.className = 'status online';
            } else {
                statusEl.textContent = '🔴 Offline - sparas lokalt';
                statusEl.className = 'status offline';
            }
        }

        function updateWordCount() {
            const len = textArea.value.length;
            const imgCount = images.length;
            wordCountEl.textContent = len + ' tecken | ' + imgCount + ' bilder';
        }

        function showToast(message) {
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        function renderImages() {
            imagePreview.innerHTML = '';
            images.forEach((img, index) => {
                const container = document.createElement('div');
                container.className = 'img-container';

                const imgEl = document.createElement('img');
                imgEl.src = img.data;

                const label = document.createElement('div');
                label.className = 'img-label';
                label.textContent = 'BILD' + (index + 1);

                container.appendChild(imgEl);
                container.appendChild(label);
                imagePreview.appendChild(container);
            });
        }

        function setupSpeechRecognition() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                dictateBtn.textContent = '⌨️ Ej tillgänglig';
                dictateBtn.disabled = true;
                return;
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'sv-SE';
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = () => {
                isRecording = true;
                dictateBtn.textContent = '⏹️ Stoppa';
                dictateBtn.classList.add('recording');
            };

            recognition.onend = () => {
                isRecording = false;
                dictateBtn.textContent = '🎤 Diktera';
                dictateBtn.classList.remove('recording');
                saveLocal();
            };

            recognition.onresult = (event) => {
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        if (textArea.value && !textArea.value.endsWith(' ')) {
                            textArea.value += ' ';
                        }
                        textArea.value += transcript;
                        saveLocal();
                    }
                }
                updateWordCount();
            };

            recognition.onerror = (event) => {
                console.error('Speech error:', event.error);
                if (event.error === 'not-allowed') {
                    showToast('Ge mikrofontillåtelse i inställningar');
                }
                isRecording = false;
                dictateBtn.textContent = '🎤 Diktera';
                dictateBtn.classList.remove('recording');
            };
        }

        function toggleDictation() {
            if (!recognition) {
                showToast('Diktering är inte tillgänglig');
                return;
            }
            if (isRecording) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }

        function takePhoto() {
            cameraInput.click();
        }

        function handlePhoto(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const imageData = e.target.result;
                const imageNum = images.length + 1;

                // Lägg till i lokal lista
                images.push({
                    num: imageNum,
                    data: imageData
                });

                // Lägg till [BILD X] i texten
                if (textArea.value && !textArea.value.endsWith(' ')) {
                    textArea.value += ' ';
                }
                textArea.value += '[BILD' + imageNum + ']';

                saveLocal();
                renderImages();
                showToast('Bild ' + imageNum + ' tillagd');
            };
            reader.readAsDataURL(file);

            // Reset input så samma fil kan väljas igen
            cameraInput.value = '';
        }

        async function saveToWord() {
            const text = textArea.value.trim();
            if (!text && images.length === 0) {
                showToast('Ingen text eller bilder att spara');
                return;
            }

            if (!navigator.onLine) {
                showToast('Kräver internet för Word-export');
                return;
            }

            saveBtn.disabled = true;
            saveBtn.textContent = '⏳ Sparar...';

            try {
                const sessionId = getSessionId();

                // Skicka texten
                if (text) {
                    await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            session_id: sessionId,
                            text: text
                        })
                    });
                }

                // Skicka bilderna
                for (let i = 0; i < images.length; i++) {
                    saveBtn.textContent = '⏳ Laddar upp bild ' + (i + 1) + '/' + images.length;
                    await fetch(IMAGE_API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            session_id: sessionId,
                            image: images[i].data
                        })
                    });
                }

                // Hämta Word-fil
                saveBtn.textContent = '⏳ Skapar Word...';
                const response = await fetch(WORD_API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: sessionId
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'anteckning-' + new Date().toISOString().slice(0,10) + '.docx';
                    a.click();
                    URL.revokeObjectURL(url);
                    showToast('Word-fil nedladdad!');

                    // Rensa efter export
                    localStorage.removeItem(SESSION_KEY);
                    getSessionId();
                } else {
                    throw new Error('Kunde inte skapa Word-fil');
                }
            } catch (error) {
                console.error('Save error:', error);
                showToast('Kunde inte spara: ' + error.message);
            } finally {
                saveBtn.disabled = false;
                saveBtn.textContent = '💾 Spara till Word';
            }
        }

        function clearText() {
            if (confirm('Vill du rensa all text och alla bilder?')) {
                textArea.value = '';
                images = [];
                localStorage.removeItem(STORAGE_KEY);
                localStorage.removeItem(IMAGES_KEY);
                localStorage.removeItem(SESSION_KEY);
                getSessionId();
                renderImages();
                updateWordCount();
                showToast('Allt rensat');
            }
        }

        // Event listeners
        dictateBtn.addEventListener('click', toggleDictation);
        photoBtn.addEventListener('click', takePhoto);
        cameraInput.addEventListener('change', handlePhoto);
        saveBtn.addEventListener('click', saveToWord);
        clearBtn.addEventListener('click', clearText);
        textArea.addEventListener('input', saveLocal);
        window.addEventListener('online', updateStatus);
        window.addEventListener('offline', updateStatus);

        // Init
        loadLocal();
        updateStatus();
        updateWordCount();
        setupSpeechRecognition();
    </script>
</body>
</html>'''

    MANIFEST = '''{
  "name": "Selatek Notes",
  "short_name": "Notes",
  "description": "Diktera och spara anteckningar med bilder",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#1a1a2e",
  "orientation": "portrait"
}'''

    @web_app.get("/")
    async def index():
        return HTMLResponse(content=INDEX_HTML)

    @web_app.get("/index.html")
    async def index_html():
        return HTMLResponse(content=INDEX_HTML)

    @web_app.get("/manifest.json")
    async def manifest():
        return Response(content=MANIFEST, media_type="application/json")

    return web_app
