import os
from flask import Flask, render_template, request, jsonify
import requests

# Configura Flask con il nome corretto al singolare (template_folder)
base_dir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(base_dir, "templates")

app = Flask(__name__, template_folder=templates_dir)

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
        url = f"https://googleapis.com{GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": user_message}]}]}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        
        bot_response = res_data['candidates']['content']['parts']['text']
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"response": "Il cervello neurale ha avuto un rallentamento. Riprova tra un istante."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
