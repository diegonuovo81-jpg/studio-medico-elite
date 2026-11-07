import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configurazione del "cervello" di Gemini tramite la variabile d'ambiente di Render
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("ATTENZIONE: Chiave API di Gemini non trovata nelle variabili d'ambiente!")

# Configurazione del modello (puoi usare gemini-1.5-flash o gemini-1.5-pro)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/", methods=["GET"])
def home():
    # Sostituisci 'index.html' con il nome del tuo file della grafica se si chiama diversamente
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"response": "Nessun messaggio ricevuto."}), 400
        
    try:
        # Prompt per dare la personalità del Dr. Martinez all'intelligenza artificiale
        prompt_medico = f"Agisci come il Dr. Diego Martinez nello Studio Medico d'Élite. Rispondi al seguente comando/messaggio: {user_message}"
        
        response = model.generate_content(prompt_medico)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Errore durante la chiamata a Gemini: {e}")
        return jsonify({"response": "Il sistema neurale ha riscontrato un errore di connessione con il modulo Gemini."}), 500

# Questo blocco assicura che Flask legga la porta corretta passata da Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
