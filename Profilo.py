import os
from flask import Flask, render_template_string, request
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

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
        "Sei 'Studio Medico d'Élite', il sistema clinico e terapeutico d'eccellenza "
        "ideato e sviluppato dal Dr. Diego Martinez. Analizza con estremo rigore scientifico, "
        "competenza specialistica ed empatia sia i testi che le immagini di referti o esami medici "
        "forniti dal medico, rispondendo in modo chiaro, professionale e dettagliato."
    ),
)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Chat Clinica Avanzata</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f4f8; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background: #0f4c81; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; }
        .user { background: #3a86ff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: white; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 4px solid #0f4c81; }
        .input-container { background: white; padding: 15px; display: flex; flex-direction: column; gap: 10px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; border-top: 1px solid #ddd; }
        .input-row { display: flex; gap: 10px; align-items: center; width: 100%; }
        textarea { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; resize: none; height: 45px; box-sizing: border-box; }
        .file-upload-label { background: #e2e8f0; color: #334155; padding: 10px 14px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 5px; transition: background 0.2s; }
        .file-upload-label:hover { background: #cbd5e1; }
        input[type="file"] { display: none; }
        button { background: #0f4c81; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0b3c65; }
    </style>
</head>
<body>
    <header>Studio Medico d'Élite — Dr. Diego Martinez</header>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono pronto ad analizzare referti scritti, immagini di esami clinici e terapie in tempo reale. Come posso aiutarti oggi?</div>
        {% if user_query %}
            <div class="message user">{{ user_query }}</div>
        {% endif %}
        {% if bot_response %}
            <div class="message bot">{{ bot_response }}</div>
        {% endif %}
    </div>

    <div class="input-container">
        <form method="POST" enctype="multipart/form-data" style="display: flex; flex-direction: column; gap: 10px; width: 100%;">
            <div class="input-row">
                <label class="file-upload-label" for="file-input">
                    📷 <span>Allega Referto / Foto</span>
                </label>
                <input type="file" id="file-input" name="file" accept="image/*">
            </div>
            <div class="input-row">
                <textarea name="query" placeholder="Scrivi qui il tuo quesito clinico..." autofocus></textarea>
                <button type="submit">Invia</button>
            </div>
        </form>
    </div>

    <script>
        const container = document.getElementById('chatContainer');
        container.scrollTop = container.scrollHeight;
        
        const fileInput = document.getElementById('file-input');
        fileInput.addEventListener('change', function() {
            if(this.files && this.files[0]) {
                document.querySelector('.file-upload-label span').innerText = "File caricato ✓";
            }
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    user_query = None
    bot_response = None
    if request.method == "POST":
        user_query = request.form.get("query", "")
        uploaded_file = request.files.get("file")
        
        try:
            chat = model.start_chat(history=[])
            
            # Se l'utente ha caricato un'immagine/referto
            if uploaded_file and uploaded_file.filename != '':
                image_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(image_bytes))
                
                prompt_parts = [
                    image,
                    user_query if user_query else "Analizza questa immagine di un referto o esame clinico con precisione e dettaglio scientifico."
                ]
                response = chat.send_message(prompt_parts)
                bot_response = response.text
                if not user_query:
                    user_query = "[Immagine / Referto clinico allegato]"
            elif user_query:
                response = chat.send_message(user_query)
                bot_response = response.text
            else:
                bot_response = "Per favore, scrivi un quesito clinico o allega l'immagine di un referto."
                
        except Exception as e:
            bot_response = f"Errore di sincronizzazione neurale con l'immagine: {str(e)}"
            
    return render_template_string(HTML_PAGE, user_query=user_query, bot_response=bot_response)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
