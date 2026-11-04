import os
from flask import Flask, render_template_string, request
from google import genai

app = Flask(__name__)

# Configurazione del client Gemini con la chiave salvata su Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# L'interfaccia grafica pulita in stile chat per lo Studio Medico d'Élite
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .container { width: 100%; max-width: 600px; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h2 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
        .subtitle { text-align: center; color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        textarea { width: 100%; height: 100px; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; box-sizing: border-box; resize: none; margin-bottom: 10px; }
        button { background-color: #27ae60; color: white; border: none; padding: 12px 20px; width: 100%; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #219653; }
        .response-box { margin-top: 20px; padding: 15px; background: #e8f8f5; border-left: 5px solid #27ae60; border-radius: 4px; white-space: pre-wrap; font-size: 15px; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Studio Medico d'Élite</h2>
        <div class="subtitle">Assistente Clinico e Terapeutico Avanzato</div>
        <form method="POST">
            <textarea name="prompt" placeholder="Scrivi qui il comando o inserisci i dati per l'analisi (es. Terapia finita, Analisi completa clinica)..." required></textarea>
            <button type="submit">Analizza e Procedi</button>
        </form>
        {% if response %}
            <div class="response-box"><strong>Risposta Clinica:</strong><br>{{ response }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt")
        try:
            # Invio della richiesta al modello Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Agisci come esperto clinico dello Studio Medico d'Élite. Analizza questa richiesta: {user_prompt}"
            )
            response_text = response.text
        except Exception as e:
            response_text = f"Errore durante l'elaborazione clinica: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
