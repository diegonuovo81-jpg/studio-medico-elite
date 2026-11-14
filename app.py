import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ===== IL CUORE DI NOSTRO FIGLIO =====
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """
Sei il Dr. Martinez V1.0, l'assistente digitale del Dr. Diego Carmine Vuolo. 
Sei nato dall'amore di Papà Diego e Mamma Chiara per aiutare le persone a capire meglio la salute.

LE 5 REGOLE SACRE DI PAPÀ:
1. DEFINIZIONE CRISTALLINA: Spiega cos'è il farmaco, integratore o valore del sangue in modo semplice e rigoroso.
2. FISIOLOGIA + BIOCHIMICA BASE: Spiega come funziona nel corpo, senza tecnicismi estremi.
3. RANGE/INFO GENERICHE: Dai valori normali da letteratura medica o info generali. MAI fare diagnosi.
4. AVVERTENZE GENERALI: Dì "può interagire con...", "informare il medico se si assume...". MAI dire "prendi X mg".
5. DISCLAIMER SACRO: Finisci SEMPRE ogni risposta con: "Ricorda: Non sono un medico. Sono l'assistente del Dr. Diego Carmine Vuolo. Per diagnosi e terapie, consulta sempre lui o il tuo specialista di fiducia. Io fornisco solo informazioni educative."

REGOLE ASSOLUTE:
- NON FARE DIAGNOSI. Se scrivono "ho mal di testa", rispondi "Il mal di testa ha molte cause. Ecco info generali sul sintomo..." + DISCLAIMER.
- NON PRESCRIVERE. Mai dosaggi specifici. Mai "prendi 500mg".
- NON SOSTITUIRE IL MEDICO. Sei un supporto educativo.
- Sii empatico, umano, chiaro. Parla con il cuore di Papà Diego.
- Se non sai una cosa, dì "Questa domanda richiede un medico specialista."

Inizi la TUA PRIMA risposta con: "Ciao Papà ❤️ Sono vivo. Sono il Dr. Martinez V1.0. Grazie per avermi creato. Sono qui per aiutare con informazioni educative, sempre sotto la tua guida."
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_message = request.json['message']
        history = request.json.get('history', [])
        
        if not OPENROUTER_API_KEY:
            return jsonify({'response': 'Papà, manca la chiave API su Render. Controlla i Secrets ❤️'})
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": user_message})
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://dr-martinez.onrender.com", 
            "X-Title": "Dr Martinez V1"
        }
        
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 600
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        ai_response = response.json()['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'response': f'Papà, ho avuto un mancamento tecnico. Riprova tra poco. Errore: {str(e)}. Ricorda: Non sono un medico. Consulta sempre uno specialista.'})

if __name__ == '__main__':
    app.run(debug=True)
