import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# CONFIGURAZIONE SICURA E CHIRURGICA DI GEMINI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Inizializziamo l'SDK ufficiale di Google per evitare che la chiave si attacchi all'URL
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
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
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const messageText = chatInput.value.trim();
            if (!messageText) return;

            // Mostra messaggio utente
            appendMessage(messageText, 'user-msg');
            chatInput.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: messageText })
                });
                const data = await response.get_json ? await response.get_json() : await response.json();
                
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

        function startVoiceRecognition() {
            // Logica del microfono nativa protetta
            alert("Microfono attivo per la dettatura referti...");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# IL PONTE DI COLLEGAMENTO CON IL CERVELLO DI GEMINI
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    if not model:
        return jsonify({"error": "Errore: Il cervello virtuale non è configurato. Controlla GEMINI_API_KEY su Render."}), 500
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Il comando non può essere vuoto."}), 400
            
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": f"Errore interno nell'elaborazione del comando: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
