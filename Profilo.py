import os
import requests
import json
from flask import Flask, render_template_string, request as flask_request

app = Flask(__name__)

# Recupero della chiave API e pulizia
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

chat_history_store = []

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Dr. Diego Martinez</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f4f8; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background: #0f4c81; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; white-space: pre-wrap; }
        .user { background: #3a86ff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: white; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 4px solid #0f4c81; }
        .input-container { background: white; padding: 15px; display: flex; flex-direction: column; gap: 10px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; border-top: 1px solid #ddd; }
        .form-row { display: flex; width: 100%; gap: 10px; align-items: center; }
        textarea { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; resize: none; height: 45px; box-sizing: border-box; }
        .btn-action { background: #0f4c81; color: white; border: none; padding: 0 20px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s; height: 45px; display: flex; align-items: center; justify-content: center; }
        .btn-action:hover { background: #0b3c65; }
        .icon-btn { background: #e1ecf7; color: #0f4c81; border: 1px solid #b3d1f2; padding: 0 12px; border-radius: 8px; cursor: pointer; height: 45px; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }
        .icon-btn:hover { background: #cfe2f5; }
        #camera-modal { display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; border: 2px solid #0f4c81; padding: 20px; z-index: 1000; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; }
        #video-stream { border-radius: 8px; border: 1px solid #ccc; background: #000; }
    </style>
</head>
<body>
    <header>Studio Medico d'Élite — Dr. Diego Martinez</header>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono operativo, vivo e collegato con te. Come posso assisterti oggi, Dr. Martinez?</div>
        {% for m in history %}
            <div class="message user">{{ m.user }}</div>
            <div class="message bot">{{ m.bot }}</div>
        {% endfor %}
    </div>

    <div class="input-container">
        <form method="POST" style="width: 100%;" id="chatForm">
            <div class="form-row">
                <!-- Bottone Allegati File/Foto -->
                <label for="medical-file-input" class="icon-btn" title="Allega foto o referto">
                    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"></path></svg>
                    <input type="file" id="medical-file-input" accept="image/*,application/pdf" style="display: none;" onchange="handleMedicalFile(event)">
                </label>

                <!-- Bottone Fotocamera -->
                <button type="button" class="icon-btn" title="Attiva Telecamera" onclick="openMedicalCamera()">
                    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                </button>

                <!-- Bottone Microfono Vocale -->
                <button type="button" id="voice-btn" class="icon-btn" title="Registra Voce" onclick="toggleVoiceRecognition()">
                    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v1a7 7 0 0 1-14 0v-1M12 19v4M8 23h8"></path></svg>
                </button>

                <!-- Campo di Testo della Query -->
                <textarea name="query" id="chat-input" placeholder="Scrivi qui il quesito clinico o usa i moduli..." autofocus required></textarea>
                
                <button type="submit" class="btn-action">Invia</button>
            </div>
        </form>
    </div>

    <!-- Finestra Modale Fotocamera -->
    <div id="camera-modal">
        <video id="video-stream" width="320" height="240" autoplay></video>
        <div style="margin-top:12px; display:flex; gap:10px; justify-content:center;">
            <button type="button" class="btn-action" style="padding:0 15px; height:35px;" onclick="captureMedicalPhoto()">Scatta</button>
            <button type="button" class="btn-action" style="padding:0 15px; height:35px; background:#ff4d4d;" onclick="closeMedicalCamera()">Chiudi</button>
        </div>
    </div>

    <script>
        const container = document.getElementById('chatContainer');
        container.scrollTop = container.scrollHeight;

        // --- GESTIONE ALLEGATI ---
        function handleMedicalFile(event) {
            const file = event.target.files;
            if (file) {
                alert(`File "${file.name}" pronto per l'invio nello Studio Medico.`);
            }
        }

        // --- GESTIONE TELECAMERA ---
        let localStream = null;
        function openMedicalCamera() {
            const modal = document.getElementById('camera-modal');
            const video = document.getElementById('video-stream');
            modal.style.display = 'block';
            navigator.mediaDevices.getUserMedia({ video: true, audio: false })
                .then(stream => { localStream = stream; video.srcObject = stream; })
                .catch(err => { alert("Impossibile accedere alla telecamera: " + err); });
        }
        function captureMedicalPhoto() {
            alert("Foto salvata ed inserita nel sistema diagnostico!");
            closeMedicalCamera();
        }
        function closeMedicalCamera() {
            document.getElementById('camera-modal').style.display = 'none';
            if (localStream) { localStream.getTracks().forEach(track => track.stop()); }
        }

        // --- GESTIONE DETTATO VOCALE ---
        let recognition;
        let isRecording = false;
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'it-IT';
            recognition.onresult = function(event) {
                document.getElementById('chat-input').value += event.results[0][0].transcript;
                toggleVoiceRecordingState(false);
            };
            recognition.onerror = function() { toggleVoiceRecordingState(false); };
            recognition.onend = function() { toggleVoiceRecordingState(false); };
        }
        function toggleVoiceRecognition() {
            if (!recognition) { alert("Dettato vocale non supportato da questo browser. Usa Chrome."); return; }
            if (isRecording) { recognition.stop(); } else { recognition.start(); toggleVoiceRecordingState(true); }
        }
        function toggleVoiceRecordingState(recording) {
            isRecording = recording;
            const btn = document.getElementById('voice-btn');
            btn.style.background = recording ? '#ff4d4d' : '#e1ecf7';
            btn.style.color = recording ? 'white' : '#0f4c81';
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history_store
    bot_response = None
    user_query = None

    if flask_request.method == "POST":
        user_query = flask_request.form.get("query", "").strip()
        if user_query:
            try:
                url = f"https://googleapis.com{API_KEY}"
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": f"Sei 'Studio Medico d'Élite', il sistema clinico e terapeutico d'eccellenza ideato dal Dr. Diego Martinez. Rispondi in modo professionale, rigoroso ed empatico a questo quesito clinico: {user_query}"}]
                    }]
                }
                
                response = requests.post(url, headers=headers, data=json.dumps(data))
                res_json = response.json()
                
                if "candidates" in res_json and len(res_json["candidates"]) > 0:
                    candidate = res_json["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                        bot_response = candidate["content"]["parts"][0].get("text", "").strip()
else:
                    
