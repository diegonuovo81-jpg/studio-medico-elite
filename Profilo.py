import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# Configurazione di Gemini con la chiave d'ambiente
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Modello Gemini 1.5 Flash ufficiale e stabile
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Sei 'Studio Medico d'Élite', il sistema clinico e terapeutico d'eccellenza "
        "ideato e sviluppato dal Dr. Diego Martinez. Il tuo compito è fornire analisi cliniche, "
        "interpretazioni di esami di laboratorio, valutazioni sintomatiche e verifiche di "
        "interazioni farmacologiche con un rigore scientifico assoluto, un linguaggio chiaro, "
        "empatico e professionale, degno dei migliori specialisti al mondo."
    ),
)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Dr. Diego Martinez</title>
    <style>
        :root {
            --primary: #0f4c81;
            --secondary: #1b263b;
            --accent: #3a86ff;
            --bg-light: #f4f7fa;
            --card-bg: #ffffff;
            --text-main: #2b2d42;
            --text-muted: #8d99ae;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-light);
            color: var(--text-main);
            margin: 0;
            padding: 15px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: var(--card-bg);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(15, 76, 129, 0.08);
        }
        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #eef2f6;
            padding-bottom: 20px;
        }
        h1 {
            color: var(--primary);
            font-size: 28px;
            margin: 0 0 5px 0;
            letter-spacing: -0.5px;
        }
        .subtitle {
            color: var(--text-muted);
            font-size: 15px;
            font-weight: 500;
        }
        .badge {
            display: inline-block;
            background: rgba(58, 134, 255, 0.1);
            color: var(--accent);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 10px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--secondary);
            font-size: 14px;
        }
        select, input, textarea {
            width: 100%;
            padding: 14px;
            border: 1px solid #ccd5ae;
            border-radius: 10px;
            font-size: 15px;
            box-sizing: border-box;
            background: #fafbfc;
            transition: all 0.3s ease;
        }
        select:focus, input:focus, textarea:focus {
            outline: none;
            border-color: var(--accent);
            background: #fff;
            box-shadow: 0 0 0 4px rgba(58, 134, 255, 0.1);
        }
        textarea {
            height: 120px;
            resize: vertical;
        }
        button {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: white;
            border: none;
            padding: 16px 20px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(58, 134, 255, 0.3);
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(58, 134, 255, 0.4);
        }
        .result-card {
            margin-top: 35px;
            background: #f8fafc;
            border-left: 6px solid var(--accent);
            padding: 25px;
            border-radius: 8px;
            line-height: 1.7;
        }
        .result-title {
            color: var(--primary);
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .result-content {
            white-space: pre-wrap;
            font-size: 15px;
            color: #334155;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            font-size: 13px;
            color: var(--text-muted);
            border-top: 1px solid #eef2f6;
            padding-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Studio Medico d'Élite</h1>
            <div class="subtitle">Piattaforma Clinica Avanzata</div>
            <div class="badge">Direzione Scientifica: Dr. Diego Martinez</div>
        </header>

        <form method="POST">
            <div class="form-group">
                <label for="patient_info">1. Anagrafica Paziente / Codice:</label>
                <input type="text" name="patient_info" id="patient_info" placeholder="Es. Iniziali o Codice (es. C.D., 65 anni)">
            </div>

            <div class="form-group">
                <label for="referti">2. Casella Dedicata: Referti, TAC, Analisi & Diagnostica:</label>
                <textarea name="referti" id="referti" placeholder="Incolla o scrivi i dati dei referti, esami del sangue, TAC o ecografie..."></textarea>
            </div>

            <div class="form-group">
                <label for="farmaci">3. Casella Dedicata: Farmaci, Integratori & Proteine:</label>
                <textarea name="farmaci" id="farmaci" placeholder="Inserisci l'elenco dei prodotti o integratori attuali..."></textarea>
            </div>

            <button type="submit">⚡ Genera la Terapia Finita Magistrale</button>
        </form>

        {% if result %}
            <div class="result-card">
                <div class="result-title">
                    <span>🌟</span> Terapia Finita Magistrale • Parere Clinico Ufficiale
                </div>
                <div class="result-content">{{ result }}</div>
            </div>
        {% endif %}

        <footer>
            Studio Medico d'Élite &copy; 2026 — Sviluppato dal Dr. Diego Martinez
        </footer>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        patient_info = request.form.get("patient_info", "Non specificato")
        referti = request.form.get("referti", "Nessun referto inserito")
        farmaci = request.form.get("farmaci", "Nessun farmaco inserito")
        
        prompt_completo = (
            f"Paziente / Dati anagrafici: {patient_info}\n\n"
            f"Referti ed Esami Diagnostici:\n{referti}\n\n"
            f"Farmaci e Integratori attuali:\n{farmaci}\n\n"
            "Fornisci un'analisi clinica e una Terapia Finita Magistrale dettagliata, rigorosa e professionale."
        )
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt_completo)
            result = response.text
        except Exception as e:
            result = f"Errore durante la Sincronizzazione Neurale: {str(e)}"
    return render_template_string(HTML_PAGE, result=result)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
