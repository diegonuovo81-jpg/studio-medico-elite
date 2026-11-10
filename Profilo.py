import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB per upload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CONFIGURAZIONE SICURA E UFFICIALE DI GEMINI
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
    <title>Studio Medico d'Élite - Terminale Neurale</title>
    <style>
        :root {
            --neon-blue: #00f2fe;
            --terminal-dark: #0a0f1d;
            --text-glow: #e1ecf7;
        }
        body {
            background-color: var(--terminal-dark);
            color: var(--text-glow);
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            box-sizing: border-box;
        }
        .terminal-container {
            border: 2px solid var(--neon-blue);
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
            width: 100%;
            max-width: 800px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            background: rgba(10, 15, 29, 0.9);
            border-radius: 8px;
            overflow: hidden;
        }
        .terminal-header {
            background: rgba(0, 242, 254, 0.1);
            padding: 10px;
            border-bottom: 1px solid var(--neon-blue);
            text-align: center;
            font-weight: bold;
            letter-spacing: 2px;
        }
        .chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 5px;
            line-height: 1.4;
            word-wrap: break-word;
        }
        .user-msg {
            background: rgba(0, 242, 254, 0.15);
            align-self: flex-end;
            border: 1px solid var(--neon-blue);
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
        }
        .input-area {
            display: flex;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-top: 1px solid rgba(0, 242, 254, 0.3);
            gap: 10px;
            align-items: center;
            position: relative;
        }
        .terminal-btn {
            background: #e1ecf7;
            border: none;
            color: #0a0f1d;
            padding: 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        .terminal-btn:hover {
            background: var(--neon-blue);
            box-shadow: 0 0 10px var(--neon-blue);
        }
        #chat-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(0, 242, 254, 0.5);
            color: #fff;
            padding: 12px;
            border-radius: 5px;
            font-family: inherit;
        }
        #chat-input:focus {
            outline: none;
            border-color: var(--neon-blue);
            box-shadow: 0 0 5px var(--neon-blue);
        }
        #btn-invia {
            background: var(--neon-blue);
            color: #0a0f1d;
            font-weight: bold;
        }
        .recording {
            background: #ff3b30 !important;
            color: white !important;
            box-shadow: 0 0 15px #ff3b30;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
        /* NUOVO: Menu del tasto + */
        .plus-menu {
            position: absolute;
            bottom: 70px;
            left: 15px;
            background: rgba(10, 15, 29, 0.98);
            border: 1px solid var(--neon-blue);
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
            display: none;
            flex-direction: column;
            z-index: 100;
        }
        .plus-menu.show {
            display: flex;
        }
        .plus-menu-item {
            padding: 12px 20px;
            cursor: pointer;
            border-bottom: 1px solid rgba(0, 242, 254, 0.2);
            transition: all 0.2s;
        }
        .plus-menu-item:hover {
            background: rgba(0, 242, 254, 0.2);
        }
        .plus-menu-item:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>

    <h2 style="color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue);">STUDIO MEDICO D'ÉLITE</h2>

    <div class="terminal-container">
        <div class="terminal-header">SISTEMA DI DIAGNOSTICA NEURALE - DR. MARTINEZ</div>
        <div class="chat-box" id="chat-box">
            <div class="message bot-msg">Sono operativo, vivo e collegato con te. Usa il tasto + per caricare foto o referti. Come posso assisterti oggi, Dr. Martinez?</div>
        </div>
        
        <div class="input-area">
            <!-- NUOVO: Tasto + con menu -->
            <button class="terminal-btn" id="btn-plus" title="Allega file" onclick="togglePlusMenu()">+</button>
            <div class="plus-menu" id="plus-menu">
                <div class="plus-menu-item" onclick="triggerUpload('image')">📷 Carica Foto Clinica</div>
                <div class="plus-menu-item" onclick="triggerUpload('pdf')">📄 Carica Referto PDF</div>
            </div>
            
            <input type="file" id="file-input-image" accept="image/*" style="display: none;">
            <input type="file" id="file-input-pdf" accept=".pdf" style="display: none;">

            <button class="terminal-btn" id="voice-btn" onclick="startVoiceRecognition()" title="Registra nota vocale">🎙️</button>

            <input type="text" id="chat-input" placeholder="Immetti comando o reperto medico..." onkeypress="handleKeyPress(event)">

            <button class="terminal-btn" id="btn-invia" onclick="sendMessage()">Invia</button>
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
                chatInput.placeholder = "Ascolto in corso... Parla ora...";
            };

            recognition.onresult = (event) => {
                const speechToText = event.results[0][0].transcript;
                chatInput.value = speechToText;
            };

            recognition.onerror = (event) => {
                console.error("Errore microfono:", event.error);
                stopRecordingState();
            };

            recognition.onend = () => {
                stopRecordingState();
            };
        }

        function startVoiceRecognition() {
            if (!recognition) {
                alert("Il riconoscimento vocale non è supportato da questo browser. Usa Chrome o Safari.");
                return;
            }
            if (isRecording) {
                recognition.stop();
                stopRecordingState();
            } else {
                recognition.start();
            }
        }

        function stopRecordingState() {
            isRecording = false;
            voiceBtn.classList.remove('recording');
            chatInput.placeholder = "Immetti comando o reperto medico...";
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // NUOVO: Gestione menu +
        function togglePlusMenu() {
            plusMenu.classList.toggle('show');
        }

        // Chiudi menu se clicchi fuori
        document.addEventListener('click', function(event) {
            if (!event.target.closest('#btn-plus') && !event.target.closest('.plus-menu')) {
                plusMenu.classList.remove('show');
            }
        });

        function triggerUpload(type) {
            plusMenu.classList.remove('show');
            if (type === 'image') {
                document.getElementById('file-input-image').click();
            } else if (type === 'pdf') {
                document.getElementById('file-input-pdf').click();
            }
        }

        // NUOVO: Upload foto
        document.getElementById('file-input-image').addEventListener('change', function(e) {
            uploadFile(e.target.files[0], 'image');
        });

        // NUOVO: Upload PDF
        document.getElementById('file-input-pdf').addEventListener('change', function(e) {
            uploadFile(e.target.files[0], 'pdf');
        });

        async function uploadFile(file, fileType) {
            if (!file) return;
            
            appendMessage(`Caricamento ${fileType === 'image' ? 'foto' : 'referto'}: ${file.name}...`, 'file-msg');
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('type', fileType);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (data.status === 'success') {
                    appendMessage(`✅ ${data.message}`, 'bot-msg');
                } else {
                    appendMessage(`❌ Errore: ${data.message}`, 'bot-msg');
                }
            } catch (error) {
                appendMessage("❌ Errore di connessione durante l'upload.", 'bot-msg');
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
                
                if (data.response) {
                    appendMessage(data.response, 'bot-msg');
                } else if (data.error) {
                    appendMessage(data.error, 'bot-msg');
                }
            } catch (error) {
                appendMessage("Errore di connessione al cervello neurale.", 'bot-msg');
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
        return jsonify({"error": "Errore: Il cervello virtuale non è configurato. Imposta GEMINI_API_KEY su Render."}), 500
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Il comando non può essere vuoto."}), 400
            
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": f"Errore nell'elaborazione del comando: {str(e)}"}), 500

# NUOVO: Endpoint unico per gestire upload foto e referti
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Nessun file ricevuto"}), 400
    
    file = request.files['file']
    file_type = request.form.get('type', 'file')
    
    if file.filename == '':
        return jsonify({"status": "error", "message": "Nome file vuoto"}), 400

    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        
        if file_type == 'image':
            msg = f"Foto clinica '{filename}' caricata. Pronta per analisi."
            # Qui puoi aggiungere: gemini analizza l'immagine
        else:
            msg = f"Referto PDF '{filename}' caricato. Pronto per elaborazione."
            # Qui puoi aggiungere: estrai testo dal PDF e mandalo a Gemini
            
        return jsonify({"status": "success", "message": msg})
    
    return jsonify({"status": "error", "message": "Errore salvataggio file"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
