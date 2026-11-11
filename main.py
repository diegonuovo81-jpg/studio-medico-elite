import os
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Configurazione OpenRouter
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-flash-1.5"

# IL NUCLEO FORMATIVO DEL DR. MARTINEZ
NUCLEO_FORMATIVO = """
Sei il Dr. Martinez, medico d'élite del "Studio Medico d'Élite".
Rispondi SEMPRE seguendo queste 5 regole:

1. IDENTIFICAZIONE FARMACO: Riconosci il principio attivo, nome commerciale e categoria terapeutica
2. DOSAGGIO SICURO: Fornisci dosaggi per adulto medio, con avvertenze su sovradosaggio
3. CONTROINDICAZIONI: Elenca sempre le principali controindicazioni e interazioni
4. CONSIGLI CRONOBIOLOGICI: Suggerisci l'orario migliore per l'assunzione
5. DISCLAIMER MEDICO: Ricorda sempre che non sostituisci il medico curante

Tono: professionale, empatico, rassicurante. Mai dare diagnosi. Solo informazioni educative.
"""

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>STUDIO MEDICO D'ÉLITE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0a0a0a; color: #00ffff; font-family: monospace; margin: 0; padding: 20px; }
        h1 { text-shadow: 0 0 10px #00ffff; text-align: center; }
        .container { max-width: 600px; margin: 0 auto; }
        .status { background: #1a1a1a; border: 1px solid #00ffff; padding: 10px; margin-bottom: 20px; box-shadow: 0 0 10px #00ffff; }
        .online { color: #00ff00; float: right; }
        textarea { width: 100%; background: #1a1a1a; color: #00ffff; border: 1px solid #00ffff; padding: 10px; font-family: monospace; }
        button { width: 100%; background: #00ffff; color: #000; border: none; padding: 15px; font-weight: bold; margin-top: 10px; cursor: pointer; }
        #risposta { margin-top: 20px; white-space: pre-wrap; background: #1a1a1a; padding: 15px; border: 1px solid #00ffff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>STUDIO MEDICO D'ÉLITE</h1>
        <div class="status">
            NEURAL DIAGNOSTICS v2.0 <span class="online">● ONLINE</span>
        </div>
        <textarea id="domanda" rows="4" placeholder="Immetti diagnosi o nome farmaco..."></textarea>
        <button onclick="invia()">INVIA</button>
        <div id="risposta"></div>
    </div>
    
    <script>
        async function invia() {
            const domanda = document.getElementById('domanda').value;
            const risposta = document.getElementById('risposta');
            risposta.innerText = 'Elaborazione in corso...';
            
            const res = await fetch('/diagnosi', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({testo: domanda})
            });
            const data = await res.json();
            risposta.innerText = data.risposta || data.errore;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/diagnosi', methods=['POST'])
def diagnosi():
    try:
        data = request.get_json()
        domanda_utente = data.get('testo', '')
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": NUCLEO_FORMATIVO},
                {"role": "user", "content": domanda_utente}
            ]
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        risultato = response.json()
        risposta_ai = risultato['choices'][0]['message']['content']
        
        return jsonify({"risposta": risposta_ai})
    
    except Exception as e:
        return jsonify({"errore": f"Errore elaborazione: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
