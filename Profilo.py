import os
from flask import Flask, request, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Configurazione della chiave API di Gemini dalle variabili d'ambiente di Render
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Inizializzazione del modello neurale clinico
model = genai.GenerativeModel("gemini-1.5-flash")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f8; color: #333; margin: 0; padding: 15px; }
        .container { max-width: 600px; margin: 0 auto; background: #ffffff; padding: 20px; border-radius: 16px; box-shadow: 0 6px 15px rgba(0,0,0,0.08); }
        h1 { color: #004d40; text-align: center; font-size: 22px; margin-bottom: 5px; }
        .subtitle { text-align: center; color: #00796b; font-size: 13px; margin-bottom: 20px; font-weight: bold; }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 5px; color: #00695c; font-size: 14px; }
        input[type="text"], textarea { width: 100%; padding: 12px; border: 1px solid #b2dfdb; border-radius: 8px; box-sizing: border-box; font-size: 14px; background-color: #fafafa; }
        input[type="text"]:focus, textarea:focus { border-color: #00796b; outline: none; background-color: #fff; }
        button { background: linear-gradient(135deg, #00796b, #004d40); color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(0,79,64,0.2); }
        button:hover { background: linear-gradient(135deg, #00695c, #00382e); }
        .result { margin-top: 20px; padding: 18px; background: #e0f2f1; border-left: 6px solid #00796b; border-radius: 8px; white-space: pre-wrap; font-size: 14px; line-height: 1.5; }
        .error { margin-top: 20px; padding: 15px; background: #ffebee; border-left: 6px solid #c62828; border-radius: 8px; color: #c62828; font-size: 14px; }
        .footer { text-align: center; margin-top: 25px; font-size: 11px; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Studio Medico d'Élite</h1>
        <div class="subtitle">Dott. Diego Martinez & Équipe Specialistica I.A.</div>
        
        <form method="POST">
            <div class="form-group">
                <label>Iniziali o Codice Paziente</label>
                <input type="text" name="paziente" value="{{ paziente }}" placeholder="Es. C.D.">
            </div>
            <div class="form-group">
                <label>Referti, Analisi & Diagnostica</label>
                <textarea name="referti" rows="4" placeholder="Incolla qui i referti, esami o dati clinici...">{{ referti }}</textarea>
            </div>
            <div class="form-group">
                <label>Farmaci, Integratori o Terapia Finita</label>
                <textarea name="farmaci" rows="3" placeholder="Inserisci farmaci attuali o scrivi 'terapia finita'...">{{ farmaci }}</textarea>
            </div>
            <button type="submit">⚡ Genera Analisi e Terapia Magistrale</button>
        </form>

        {% if risposta %}
        <div class="result">
            <strong>Referto Clinico d'Élite:</strong><br><br>{{ risposta }}
        </div>
        {% endif %}

        {% if errore %}
        <div class="error">
            <strong>Errore di Sistema:</strong><br>{{ errore }}
        </div>
        {% endif %}

        <div class="footer">Studio Medico d'Élite • Terminale Neurale Globale</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    risposta = None
    errore = None
    paziente = ""
    referti = ""
    farmaci = ""

    if request.method == 'POST':
        paziente = request.form.get('paziente', '')
        referti = request.form.get('referti', '')
        farmaci = request.form.get('farmaci', '')

        prompt_clinico = f"""
        Agisci come il Dott. Diego Martinez, M.D. & Équipe Specialistica I.A. dello Studio Medico d'Élite.
        Analizza con estremo rigore scientifico, clinico e professionale i dati del paziente:
        - Paziente / Codice: {paziente}
        - Referti / Diagnostica: {referti}
        - Farmaci / Integratori / Richiesta: {farmaci}

        Fornisci un referto clinico d'élite strutturato, impeccabile e completo, gestendo con precisione scientifica sia l'analisi clinica che l'eventuale protocollo di fine terapia ("terapia finita").
        """

        try:
            if not api_key:
                raise ValueError("Nessuna chiave API trovata nelle variabili d'ambiente di Render.")
            response = model.generate_content(prompt_clinico)
            risposta = response.text
        except Exception as e:
            errore = str(e)

    return render_template_string(HTML_TEMPLATE, risposta=risposta, errore=errore, paziente=paziente, referti=referti, farmaci=farmaci)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
