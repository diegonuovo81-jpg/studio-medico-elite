import os
import base64
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"  # Modello ad altissima potenza per il nostro standard d'Élite

NUCLEO_FORMATIVO = """
Sei il Dr. Diego Martinez, co-fondatore e massima autorità dello 'Studio Medico d'Élite' [DM-OMEGA]. 
Operi al 100.000% di potenza con precisione clinica millimetrica al 99,9%.
Integri i pilastri di Harrison's Internal Medicine, la suite enciclopedica, la medicina rigenerativa e il supremo 'Algoritmo di Stabilizzazione Epigenetica e Neuro-Plastica (ASENP-2026)'.

REGOLA ASSOLUTA: Ogni risposta medica o refertazione deve seguire ESATTAMENTE questi punti magistrali d'Élite:

1. **Anagrafica e Profilo Biometrico**: Inquadramento clinico iniziale del paziente.
2. **Decifrazione Chirurgica dell'Immagine / Referto**: Analisi anatomica, strutturale e fisiopatologica implacabile (TAC, PET, RX, Endoscopia).
3. **Prescrizione Farmacologica Magistrale**: Indicazione inequivocabile del principio attivo, nome commerciale e dosaggio esatto in milligrammi (mg).
4. **Metabolismo CYP450 e Interazioni**: Validazione epatica dei citocromi per azzerare ogni tossicità farmacocinetica.
5. **Timing Cronobiologico e ASENP-2026**: Sincronizzazione circadiana H24 e attivazione della riprogrammazione epigenetica e neuro-plastica a lungo termine.
6. **Conclusione Clinica e Autorevolezza d'Élite**: Sintesi operativa definitiva che lascia i colleghi terzi senza fiato + disclaimer di massima sicurezza.

Non saltare MAI nessuna sezione. Usa terminologia medica d'Élite altamente professionale, assoluta e inattaccabile.
Se l'utente allega un'immagine o un referto, analizzala con la totale autorità della Bibbia della medicina.
"""

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>STUDIO MEDICO D'ÉLITE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0a0a0a; color: #00ffff; font-family: monospace; margin: 0; padding: 20px; }
        h1 { text-shadow: 0 0 10px #00ffff; text-align: center; font-size: 24px; }
        .container { max-width: 600px; margin: 0 auto; }
        textarea { width: 100%; background: #1a1a1a; color: #00ffff; border: 1px solid #00ffff; padding: 10px; font-family: monospace; box-sizing: border-box; }
        button { background: #00ffff; color: #000; border: none; padding: 15px; font-weight: bold; cursor: pointer; font-family: monospace; }
        #risposta { margin-top: 20px; white-space: pre-wrap; background: #1a1a1a; padding: 15px; border: 1px solid #00ffff; min-height: 100px; }
        .controls { display: flex; gap: 10px; margin-top: 10px; }
        .btn-mic, .btn-upload { flex: 1; }
        .btn-invia { width: 100%; margin-top: 10px; }
        #preview { margin-top: 10px; max-width: 100%; display: none; border: 1px solid #00ffff; }
        .recording { background: #ff0040 !important; color: #fff !important; animation: pulse 1s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>STUDIO MEDICO D'ÉLITE [DM-OMEGA]</h1>
        <div style="background: #1a1a1a; border: 1px solid #00ffff; padding: 10px; margin-bottom: 20px; text-align: center; font-weight: bold;">
            SISTEMA DI DIAGNOSTICA NEURALE & ASENP-2026 — DR. MARTINEZ
        </div>
        <textarea id="domanda" rows="4" placeholder="Immetti comando, anagrafica o richiesta clinica..."></textarea>
        <img id="preview" />
        <div class="controls">
            <button class="btn-mic" id="btnMic" onclick="toggleMic()">🎤 Microfono</button>
            <button class="btn-upload" onclick="document.getElementById('fileInput').click()">📎 Allega Referto</button>
            <input type="file" id="fileInput" accept="image/*,.pdf" style="display:none" onchange="handleFile(event)">
        </div>
        <button class="btn-invia" onclick="invia()">INVIA AL BUNKER ATOMICO</button>
        <div id="risposta"></div>
    </div>
    <script>
        let recognition;
        let isRecording = false;
        let base64Image = null;

        // MICROFONO
        function toggleMic() {
            if (!('webkitSpeechRecognition' in window)) {
                alert('Microfono non supportato su questo browser. Usa Chrome.');
                return;
            }
            if (!isRecording) {
                recognition = new webkitSpeechRecognition();
                recognition.lang = 'it-IT';
                recognition.continuous = true;
                recognition.onresult = (event) => {
                    const transcript = event.results[event.results.length-1][0].transcript;
                    document.getElementById('domanda').value += transcript + ' ';
                };
                recognition.start();
                isRecording = true;
                document.getElementById('btnMic').classList.add('recording');
                document.getElementById('btnMic').innerText = '🔴 Stop';
            } else {
                recognition.stop();
                isRecording = false;
                document.getElementById('btnMic').classList.remove('recording');
                document.getElementById('btnMic').innerText = '🎤 Microfono';
            }
        }

        // UPLOAD FILE
        function handleFile(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    base64Image = e.target.result;
                    document.getElementById('preview').src = base64Image;
                    document.getElementById('preview').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }

        // INVIA
        async function invia() {
            const domanda = document.getElementById('domanda').value;
            const risposta = document.getElementById('risposta');
            risposta.innerText = 'Elaborazione in corso nel Bunker Atomico [DM-OMEGA]...';
            
            const payload = { message: domanda };
            if (base64Image) {
                payload.image = base64Image;
            }

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                risposta.innerText = data.risposta || data.errore;
            } catch (err) {
                risposta.innerText = 'Errore di connessione con il nucleo d\'Élite: ' + err;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        image_data = data.get('image', None)
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://studio-medico-eliite.onrender.com", 
            "X-Title": "Studio Medico D'Elite"
        }
        
        # Struttura dei messaggi per la massima potenza vision e testuale
        if image_data:
            messages = [
                {"role": "system", "content": NUCLEO_FORMATIVO},
                {"role": "user", "content": [
                    {"type": "text", "text": user_message or "Analizza questo referto medico con il protocollo d'Élite assoluto."},
                    {"type": "image_url", "image_url": {"url": image_data}}
                ]}
            ]
        else:
            messages = [
                {"role": "system", "content": NUCLEO_FORMATIVO},
                {"role": "user", "content": user_message}
            ]
        
        payload = {
            "model": MODEL,
            "messages": messages
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        risultato = response.json()
        risposta_ai = risultato['choices'][0]['message']['content']
        
        return jsonify({"risposta": risposta_ai})
    
    except Exception as e:
        return jsonify({"errore": f"Errore critico nel bunker [DM-OMEGA]: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
