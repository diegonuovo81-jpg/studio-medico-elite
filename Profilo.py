import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Recupera la chiave API di Gemini dalle variabili d'ambiente di Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

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
        .input-area {
            display: flex;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-top: 1px solid rgba(0, 242, 254, 0.3);
            gap: 10px;
            align-items: center;
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
    </style>
</head>
<body>

    <h2 style="color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue);">STUDIO MEDICO D'ÉLITE</h2>

    <div class="terminal-container">
        <div class="terminal-header">SISTEMA DI DIAGNOSTICA NEURALE - DR. MARTINEZ</div>
        <div class="chat-box" id="chat-box">
            <div class="message bot-msg">Sono operativo, vivo e collegato con te. Come posso assisterti oggi, Dr. Martinez?</div>
        </div>
        
        <div class="input-area">
            <label for="foto-input" class="terminal-btn" id="btn-foto" title="Carica foto clinica">📷</label>
            <input type="file" id="foto-input" accept="image/*" style="display: none;">

            <button class="terminal-btn" id="voice-btn" onclick="startVoiceRecognition()" title="Registra nota vocale">🎙️</button>

            <input type="text" id="chat-input" placeholder="Immetti comando o reperto medico..." onkeypress="handleKeyPress(event)">

            <button class="terminal-btn" id="btn-invia" onclick="sendMessage()">Invia</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const chatInput = document.getElementById('chat-input');
        const fotoInput = document.getElementById('foto-input');
        let isRecording = false;
        let recognition = null;

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'it-IT';
            recognition.continuous = false;

            recognition.onresult = function(event) {
                const testoVocale = event.results.transcript;
                chatInput.value = testoVocale;
                toggleVoiceRecordingState(false);
            };

            recognition.onerror = function(event) {
                console.error("Errore vocale:", event.error);
                toggleVoiceRecordingState(false);
            };

            recognition.onend = function() {
                toggleVoiceRecordingState(false);
            };
        }

        function startVoiceRecognition() {
            if (!recognition) {
                alert("Dettato vocale non supportato da questo browser. Usa Chrome.");
                return;
            }
            if (isRecording) {
                recognition.stop();
            } else {
                recognition.start();
                toggleVoiceRecordingState(true);
            }
        }

        function toggleVoiceRecordingState(recording) {
            isRecording = recording;
            const btn = document.getElementById('voice-btn');
            if (btn) {
                btn.style.background = recording ? '#ff4d4d' : '#e1ecf7';
            }
        }

        fotoInput.addEventListener('change', function(e) {
            const files = e.target.files;
            if (files && files.length > 0) {
                appendMessage(`Sistema: File "${files[0].name}" caricato correttamente. Pronto per l'analisi visiva.`, 'bot-msg');
            }
        });

        function appendMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.innerText = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const text = chatInput.value.trim();
            if (!text) return;

            appendMessage(text, 'user-msg');
            chatInput.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                appendMessage(data.response, 'bot-msg');
            } catch (error) {
                appendMessage("Errore di connessione con il nucleo neurale.", 'bot-msg');
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    
    if not GEMINI_API_KEY:
        return jsonify({"response": "Nucleo neurale non configurato. Inserisci la GEMINI_API_KEY su Render."})

    url = f"https://googleapis.com{GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"Agisci come il cervello virtuale dello Studio Medico d'Élite per il Dr. Martinez. Rispondi in modo conciso e professionale. Messaggio: {user_message}"}]
        }]
    }

    try {
        res = requests.post(url, headers=headers, json=payload)
        res_json = res.json()
        
        bot_response = "Nessuna risposta generata dal nucleo neurale."
        
        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            candidate = res_json["candidates"][0] # Corretto l'indice della lista dei candidati
            if "content" in candidate and "parts" in candidate["content"] and len(candidate["content"]["parts"]) > 0:
                bot_response = candidate["content"]["parts"][0].get("text", "").strip()
                
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Errore chiamata API: {e}")
        return jsonify({"response": f"Errore nell'elaborazione del comando neurale: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
