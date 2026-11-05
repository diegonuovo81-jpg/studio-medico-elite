import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# Configurazione di Gemini con la chiave d'ambiente
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Modello Gemini 1.5 Flash
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Sei 'Studio Medico d'Élite', un assistente clinico e terapeutico di altissimo livello "
        "al fianco del Dr. Diego Martinez. Analizzi referti, immagini e dati di laboratorio "
        "fornendo un'analisi clinica rigorosa, dettagliata e verificando con attenzione "
        "eventuali interazioni farmacologiche."
    ),
)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f4f8; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1 { color: #0f4c81; text-align: center; font-size: 24px; margin-bottom: 5px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        textarea { width: 100%; height: 150px; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; box-sizing: border-box; margin-bottom: 15px; }
        button { background: #0f4c81; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; transition: background 0.2s; }
        button:hover { background: #0b3c65; }
        .result { margin-top: 30px; background: #f8fafc; border-left: 5px solid #0f4c81; padding: 20px; border-radius: 4px; line-height: 1.6; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Studio Medico d'Élite</h1>
        <div class="subtitle">Dr. Diego Martinez — Assistente Clinico Avanzato</div>
        <form method="POST">
            <textarea name="query" placeholder="Inserisci qui i referti, i dati di laboratorio o i farmaci da analizzare..."></textarea>
            <button type="submit">Esegui Analisi Clinica</button>
        </form>
        {% if result %}
            <div class="result"><strong>Analisi e Parere Medico:</strong><br><br>{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_query = request.form.get("query")
        if user_query:
            try:
                chat = model.start_chat(history=[])
                response = chat.send_message(user_query)
                result = response.text
            except Exception as e:
                result = f"Errore durante l'elaborazione dell'analisi: {str(e)}"
    return render_template_string(HTML_PAGE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

