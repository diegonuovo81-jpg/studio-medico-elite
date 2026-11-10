import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite - Terminale Neurale v2.0</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;400&display=swap');
        
        :root {
            --neon-blue: #00f2fe;
            --neon-purple: #8a2be2;
            --terminal-dark: #050a14;
            --text-glow: #e1ecf7;
            --danger-red: #ff3b30;
        }
        * { box-sizing: border-box; }
        body {
            background: radial-gradient(ellipse at center, #0a0f1d 0%, #050a14 100%);
            color: var(--text-glow);
            font-family: 'Roboto Mono', monospace;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: repeating-linear-gradient(0deg, rgba(0,0,0,0.15), rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px);
            pointer-events: none;
            z-index: 1;
        }
        h2 {
            font-family: 'Orbitron', sans-serif;
            color: var(--neon-blue);
            text-shadow: 0 0 10px var(--neon-blue), 0 0 20px var(--neon-blue), 0 0 30px var(--neon-purple);
            letter-spacing: 3px;
            margin-bottom: 20px;
            z-index: 2;
            animation: flicker 3s infinite alternate;
        }
        @keyframes flicker {
            0%, 18%, 22%, 25%, 53%, 57%, 100% { opacity: 1; }
            20%, 24%, 55% { opacity: 0.8; }
        }
        .terminal-container {
            border: 2px solid var(--neon-blue);
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.3), inset 0 0 15px rgba(0, 242, 254, 0.1);
            width: 100%;
            max-width: 900px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            background: rgba(5, 10, 20, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            overflow: hidden;
            z-index: 2;
            animation: bootup 1s ease-out;
        }
        @keyframes bootup {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        .terminal-header {
            background: linear-gradient(90deg, rgba(0, 242, 254, 0.2), rgba(138, 43, 226, 0.2));
            padding: 12px;
            border-bottom: 1px solid var(--neon-blue);
            text-align: center;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            letter-spacing: 2px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-dot {
            width: 10px; height: 10px;
            background: #00ff41;
            border-radius: 50%;
            box-shadow: 0 0 10px #00ff41;
            animation: pulse 2s infinite;
        }
        .chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .chat-box::-webkit-scrollbar { width: 6px; }
        .chat-box::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
        .chat-box::-webkit-scrollbar-thumb { background: var(--neon-blue); border-radius: 3px; }
        .message {
            max-width: 80%;
            padding: 12px 18px;
            border-radius: 8px;
            line-height: 1.5;
            word-wrap: break-word;
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-msg {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(138, 43, 226, 0.2));
            align-self: flex-end;
            border: 1px solid var(--neon-blue);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        }
        .bot-msg {
            background: rgba(255, 255, 255, 0.05);
            align-self: flex-start;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .file-msg {
            background: rgba(255, 193, 7, 0.15);
            align-self: flex-end;
            border: 1px solid #ffc107;
            font-style: italic;
            box-shadow: 0 0 10px rgba(255, 193, 7, 0.2);
        }
        .input-area {
            display: flex;
            padding: 15px;
            background: rgba(0, 0, 0, 0.4);
            border-top: 1px solid rgba(0, 242, 254, 0.3);
            gap: 10px;
            align-items: center;
            position: relative;
        }
        .terminal-btn {
            background: linear-gradient(135deg, #e1ecf7, #b8d4f0);
            border: none;
            color: #0a0f1d;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        .terminal-btn:hover {
            background: var(--neon-blue);
            box-shadow: 0 0 15px var(--neon-blue);
            transform: translateY(-2px);
        }
        #chat-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(0, 242, 254, 0.5);
            color: #fff;
            padding: 14px;
            border-radius: 8px;
            font-family: 'Roboto Mono', monospace;
            transition: all 0.3s;
        }
        #chat-input:focus {
            outline: none;
            border-color: var(--neon-blue);
            box-shadow: 0 0 10px var(--neon-blue), inset 0 0 5px rgba(0, 242, 254, 0.2);
        }
        #btn-invia {
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
            color: #fff;
            text-shadow: 0 0 5px rgba(0,0,0,0.5);
        }
        .recording {
            background: var(--danger-red) !important;
            color: white !important;
            box-shadow: 0 0 20px var(--danger-red) !important;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.05); }
        }
        .plus-menu {
            position: absolute;
            bottom: 75px;
            left: 15px;
            background: rgba(5, 10, 20, 0.98);
            border: 1px solid var(--neon-blue);
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            display: none;
            flex-direction: column;
            z-index: 100;
            overflow: hidden;
        }
        .plus-menu.show { display: flex; animation: menuPop 0.2s ease-out; }
        @keyframes menuPop {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .plus-menu-item {
            padding: 14px 24px;
            cursor: pointer;
            border-bottom: 1px solid rgba(0, 242, 254, 0.2);
            transition: all 0.2s;
            white-space: nowrap;
        }
        .plus-menu-item:hover {
            background: linear-gradient(90deg, rgba(0, 242, 254, 0.3), transparent);
            padding-left: 28px;
        }
        .plus-menu-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <h2>STUDIO MEDICO D'ÉLITE</h2>
    <div class="terminal-container">
        <div class="terminal-header">
            <span>NEURAL DIAGNOSTICS v2.0</span>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 0.8rem;">ONLINE</span>
                <div class="status-dot"></div>
            </div>
        </div>
        <div class="chat-box" id="chat-box">
            <div class="message bot-msg">Sistema inizializzato. Motore neurale Gemini attivo. Premi + per caricare foto cliniche o referti PDF. In attesa di comandi, Dr. Martinez.</div>
        </div>
        <div class="input-area">
            <button class="terminal-btn" id="btn-plus" title="Allega file" onclick="togglePlusMenu()">+</button>
            <div class="plus-menu" id="plus-menu">
                <div class="plus-menu-item" onclick="triggerUpload('image')">📷 Foto Clinica</div>
                <div class="plus-menu-item" onclick="triggerUpload('pdf')">📄 Referto PDF</div>
            </div>
            <input type="file" id="file-input-image" accept="image/*" style="display: none;">
            <input type="file" id="file-input-pdf" accept=".pdf" style="display: none;">
            <button class="terminal-btn" id="voice-btn" onclick="startVoiceRecognition()" title="Nota vocale">🎙️</button>
            <input type="text" id="chat-input" placeholder="Immetti diagnosi o comando..." onkeypress="handleKeyPress(event)">
            <button class="terminal-btn" id="btn-invia" onclick="sendMessage()">INVIA</button>
        </div>
    </div>
    <script>
        const chatBox = document.getElementById('chat-box');
        const chatInput = document.getElementById('chat-input');
        const voiceBtn = document.getElementById('voice-btn');
        const plusMenu = document.getElementById('plus-menu');
        let isRecording = false;
        let recognition = null;

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'it-IT';
            recognition.interimResults = false;
            recognition.onstart = () => {
                isRecording = true;
                voiceBtn.classList.add('recording');
                chatInput.placeholder = "Ascolto attivo...";
            };
            recognition.onresult = (event) => {
                chatInput.value = event.results[0][0].transcript;
            };
            recognition.onerror = () => stopRecordingState();
            recognition.onend = () => stopRecordingState();
        }

        function startVoiceRecognition() {
            if (!recognition) return alert("Browser non supportato. Usa Chrome.");
            if (isRecording) recognition.stop();
            else recognition.start();
        }
        function stopRecordingState() {
            isRecording = false;
            voiceBtn.classList.remove('recording');
            chatInput.placeholder = "Immetti diagnosi o comando...";
        }
        function handleKeyPress(event) {
            if (event.key === 'Enter') sendMessage();
        }
        function togglePlusMenu() {
            plusMenu.classList.toggle('show');
        }
        document.addEventListener('click', function(event) {
            if (!event.target.closest('#btn-plus') && !event.target.closest('.plus-menu')) {
                plusMenu.classList.remove('show');
            }
        });
        function triggerUpload(type) {
            plusMenu.classList.remove('show');
            document.getElementById(type === 'image' ? 'file-input-image' : 'file-input-pdf').click();
        }
        document.getElementById('file-input-image').addEventListener('change', e => uploadFile(e.target.files[0], 'image'));
        document.getElementById('file-input-pdf').addEventListener('change', e => uploadFile(e.target.files[0], 'pdf'));

        async function uploadFile(file, fileType) {
            if (!file) return;
            appendMessage(`Upload: ${file.name}...`, 'file-msg');
            const formData = new FormData();
            formData.append('file', file);
            formData.append('type', fileType);
            try {
                const response = await fetch('/upload', { method: 'POST', body: formData });
                const data = await response.json();
                appendMessage(data.status === 'success' ? `✅ ${data.message}` : `❌ ${data.message}`, 'bot-msg');
            } catch (error) {
                appendMessage("❌ Errore connessione upload.", 'bot-msg');
            }
        }
        async function sendMessage() {
            const messageText = chatInput.value.trim();
            if (!messageText) return;
            appendMessage(messageText, 'user-msg');
            chatInput.value = '';
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: messageText })
                });
                const data = await response.json();
                appendMessage(data.response || data.error || "Errore sconosciuto", 'bot-msg');
            } catch (error) {
                appendMessage("Errore connessione neurale.", 'bot-msg');
            }
        }
        function appendMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.innerText = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    if not model:
        return jsonify({"error": "Errore: GEMINI_API_KEY non configurata su Render."}), 500
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Comando vuoto."}), 400
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": f"Errore elaborazione: {str(e)}"}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Nessun file"}), 400
    file = request.files['file']
    file_type = request.form.get('type', 'file')
    if file.filename == '':
        return jsonify({"status": "error", "message": "Nome file vuoto"}), 400
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        msg = f"Foto '{filename}' caricata nel database." if file_type == 'image' else f"Referto '{filename}' archiviato."
        return jsonify({"status": "success", "message": msg})
    return jsonify({"status": "error", "message": "Errore salvataggio"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
