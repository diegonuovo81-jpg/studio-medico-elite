import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Recupera la chiave API dalle variabili d'ambiente di Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if not GEMINI_API_KEY:
        return jsonify({"response": "Errore: Chiave API di Gemini non configurata nel server Render."})
    
    try:
        # Chiamata HTTP diretta e leggera per non sovraccaricare il server
        url = f"https://googleapis.com{GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": user_message}]}]}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        
        bot_response = res_data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"response": "Il cervello neurale ha avuto un rallentamento. Riprova tra un istante."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
