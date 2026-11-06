
import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Recupera la chiave API dalle variabili d'ambiente di Render
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    # Configurazione del modello Gemini
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
else:
    model = None

@app.route("/")
def index():
    # Restituisce la pagina principale del terminale
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not model:
        return jsonify({"error": "Modello non configurato. Controlla la chiave API su Render."}), 500
    
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Messaggio vuoto."}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
