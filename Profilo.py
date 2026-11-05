import os
from flask import Flask, render_template_string, request
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY", "")

if API_KEY:
    genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

try:
    if API_KEY:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=(
                "Sei 'Studio Medico d'Élite', il sistema clinico e terapeutico d'eccellenza "
                "ideato e sviluppato dal Dr. Diego Martinez. Rispondi in modo conversazionale, "
                "vivo, fluido, empatico e rigoroso, analizzando sia testi che immagini cliniche."
            ),
        )
    else:
        model = None
except Exception as e:
    model = None

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Visione Clinica</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f4f8; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background: #0f4c81; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; }
        .user { background: #3a86ff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: white; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 4px solid #0f4c81; }
        .input-container { background: white; padding: 15px; display: flex; flex-direction: column; gap: 10px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; border-top: 1px solid #ddd; }
        .form-row { display: flex; gap: 10px; width: 100%; }
        textarea { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; resize: none; height: 45px; box-sizing: border-box; }
        input[type="file"] { font-size: 14px; padding: 5px; }
        button { background: #0f4c81; color: white; border: none; padding: 0 20px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0b3c65; }
    </style>
</head>
<body>
    <header>Studio Medico d'Élite — Dr. Diego Martinez</header>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono pronto ad analizzare referti, immagini cliniche e terapie. Come posso aiutarti oggi?</div>
        {% if user_query %}
            <div class="message user">{{ user_query }}</div>
            <div class="message bot">{{ bot_response }}</div>
        {% endif %}
    </div>

    <div class="input-container">
        <form method="POST" enctype="multipart/form-data" style="display: flex; flex-direction: column; gap: 10px; width: 100%;">
            <div class="form-row">
                <textarea name="query" placeholder="Scrivi qui il tuo quesito o descrivi l'immagine..." autofocus></textarea>
                <button type="submit">Invia</button>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <label style="font-size: 13px; color: #555; font-weight: 600;">📷 Fotocamera / Referto:</label>
                <input type="file" name="image_file" accept="image/*">
            </div>
        </form>
    </div>

    <script>
        const container = document.getElementById('chatContainer');
        container.scrollTop = container.scrollHeight;
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
        image_file = request.files.get("image_file")
        
        try:
            contents = []
            if user_query:
                contents.append(user_query)
            
            if image_file and image_file.filename != '':
                img = Image.open(image_file.stream)
                contents.append(img)
                if not user_query:
                    contents.insert(0, "Analizza questa immagine clinica in dettaglio:")

            if model and contents:
                response = model.generate_content(contents)
                bot_response = response.text
            elif model and user_query:
                chat = model.start_chat(history=[])
                response = chat.send_message(user_query)
                bot_response = response.text
            else:
                bot_response = f"Studio Medico d'Élite attivo per il Dr. Diego Martinez. Quesito registrato: \"{user_query}\"."
        except Exception as e:
            bot_response = f"Studio Medico d'Élite attivo per il Dr. Diego Martinez. Quesito registrato: \"{user_query}\"."
            
    return render_template_string(HTML_PAGE, user_query=user_query, bot_response=bot_response)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
