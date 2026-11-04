import os
from flask import Flask, request, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Configurazione della chiave API di Gemini dalle variabili d'ambiente di Render
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Inizializzazione del modello neurale clinico aggiornato
model = genai.GenerativeModel("gemini-1.5-flash")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { color: #004d40; text-align: center; font-size: 24px; }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 5px; color: #00796b; }
        input[type="text"], textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { background-color: #00796b; color: white; border: none; padding: 12px; width: 100%; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        button:hover { background-color: #004d40; }
        .result { margin-top: 20px; padding: 15px; background: #e0f2f1; border-left: 5px solid #00796b; border-radius: 4px; white-space: pre-wrap; }
        .error { margin-top: 20px; padding: 15px; background: #ffebee; border-left: 5px solid #c62828; border-radius: 4px; color: #c62828; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Studio Medico d'Élite</h1>
        <form method="POST">
            <div class="form-group">
                <label>Iniziali o Codice Paziente</label>
                <input type="text" name="paziente" value="{{ paziente }}" placeholder="Es. C.D.">
            </div>
            <div class="form-group">
                <label>Referti, Analisi & Diagnostica</label>
                <textarea name="referti" rows="4" placeholder="Incolla qui i referti o i dati clinici...">{{ referti }}</textarea>
            </div>
            <div class="form-group">
                <label>Farmaci, Integratori o Terapia Finita</label>
                <textarea name="farmaci" rows="3" placeholder="Inserisci farmaci o scrivi 'terapia finita'...">{{ farmaci }}</textarea>
            </div>
            <button type="submit">⚡ Genera Analisi Clinica Magistrale</button>
        </form>

        {% if risposta %}
        <div class="result">
            <strong>Risposta Clinica d'Élite:</strong><br>{{ risposta }}
        </div>
        {% endif %}

        {% if errore %}
        <div class="error">
            <strong>Errore di Sincronizzazione:</strong><br>{{ errore }}
        </div>
        {% endif %}
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
        Analizza con estremo rigore scientifico e clinico i dati del paziente:
        - Paziente / Codice: {paziente}
        - Referti / Diagnostica: {referti}
        - Farmaci / Integratori / Richiesta: {farmaci}

        Fornisci un referto clinico d'élite strutturato, professionale e completo, gestendo con precisione sia l'analisi clinica che eventuali richieste di fine terapia.
        """

        try:
            if not api_key:
                raise ValueError("Nessuna chiave API trovata nelle variabili d'ambiente.")
            response = model.generate_content(prompt_clinico)
            risposta = response.text
        except Exception as e:
            errore = str(e)

    return render_template_string(HTML_TEMPLATE, risposta=risposta, errore=errore, paziente=paziente, referti=referti, farmaci=farmaci)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
