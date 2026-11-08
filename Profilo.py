import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Evita blocchi di sicurezza tra frontend e backend
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Permette al terminale web di comunicare liberamente con Flask

# 1. Recupera la chiave API in modo sicuro da Render
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("ERRORE: GEMINI_API_KEY non configurata su Render!")

@app.route("/")
def index():
    # Se il tuo file HTML si chiama index.html ed è nella cartella 'templates'
    return render_template("index.html")

# 2. Questa è la rotta che il tuo terminale userà per inviare i messaggi
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Messaggio mancante"}), 400
        
    user_message = data["message"]
    
    if not API_KEY:
        return jsonify({"answer": "Errore di sistema: Cervello virtuale non collegato (Chiave API mancante su Render)."}), 500

    try:
        # Usiamo il modello standard ultra-veloce per le chat
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="Sei il Dr. Diego Martinez, titolare dello Studio Medico d'Élite. Rispondi usando un tono professionale, distaccato ma estremamente intelligente, coerente con l'interfaccia a terminale neurale."
        )
        
        response = model.generate_content(user_message)
        return jsonify({"answer": response.text})
        
    except Exception as e:
        return jsonify({"error": f"Errore durante l'elaborazione: {str(e)}"}), 500

if __name__ == "__main__":
    # Render assegna una porta dinamica, questo assicura che Flask la legga correttamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
