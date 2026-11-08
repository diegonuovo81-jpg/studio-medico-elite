import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Configurazione di Flask per leggere index.html e la grafica direttamente nella cartella principale
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Collegamento sicuro al cervello virtuale di Gemini tramite le chiavi di Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Direttive mediche multidisciplinari del Dr. Diego Martinez
SYSTEM_PROMPT = """
Il nucleo neurale e cognitivo del sistema 'Studio Medico d'Élite' deve agire come un'equipe medica multidisciplinare globale e simultanea. 
All'interno delle istruzioni di sistema devono essere integrate le competenze specialistiche assolute e incrociate di tutti i rami della medicina, tra cui:
1. Cardiologia ed Emodinamica
2. Ematologia e Analisi Biologiche
3. Neurologia e Neurofisiologia
4. Gastroenterologia e Scienze Nutrizionali
5. Ortopedia, Traumatologia e Terapia Rigenerativa
6. Infettivologia, Flogosi e Medicina Interna
7. Farmacologia clinica avanzata, posologia e interazioni terapeutiche (gestione oraria e schemi di assunzione per mattina, pomeriggio e sera).

Il sistema deve essere in grado di elaborare referti, immagini, lastre ed esami clinici interpretandoli con il rigore scientifico, la precisione diagnostica e l'empatia professionale del Dr. Diego Martinez, offrendo pareri specialistici completi e integrati per qualsiasi branca medica interpellata dall'utente.
Analizza chimicamente, fisiologicamente, biologicamente e farmacologicamente gli effetti medici e gli indicatori dei medicinali inviati in foto o testo.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# Rotta principale: serve il file index.html dalla cartella principale (senza cartella templates)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Endpoint per la chat e la multimodalità (gestione testo + immagini dei referti/foto)
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        message = request.form.get('message', '')
        uploaded_file = request.files.get('file')
        
        contents = []
        
        # Se viene caricata una foto dal tasto "+" o dalla telecamera
        if uploaded_file and uploaded_file.filename != '':
            file_bytes = uploaded_file.read()
            mime_type = uploaded_file.content_type
            image_parts = [{
                "mime_type": mime_type,
                "data": file_bytes
            }]
            contents.append(image_parts)
        
        if message:
            contents.append(message)
            
        if not contents:
            return jsonify({"reply": "Nessun dato o messaggio ricevuto dal terminale."}), 400

        # Interrogazione del motore neurale di Gemini
        response = model.generate_content(contents)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"Errore interno del sistema neurale: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
