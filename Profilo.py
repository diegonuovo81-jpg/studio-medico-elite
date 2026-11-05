import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# CHIAVE API INTEGRATA DIRETTAMENTE NEL CODICE PER MASSIMA STABILITÀ
GEMINI_API_KEY = "AIzaSyD-Tu_chiave_gia_inserita_e_protetta"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
        "ideato e sviluppato dal Dr. Diego Martinez. Rispondi in modo conversazionale, "
        "vivo, fluido, empatico e rigoroso, esattamente come un medico specialista "
        "e un assistente IA di altissimo livello."
    ),
)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Chat Clinica</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f4f8; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background: #0f4c81; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; }
        .user { background: #3a86ff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: white; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 4px solid #0f4c81; }
        .input-container { background: white; padding: 15px; display: flex; gap: 10px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; border-top: 1px solid #ddd; }
        textarea { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; resize: none; height: 45px; box-sizing: border-box; }
        button { background: #0f4c81; color: white; border: none; padding: 0 20px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0b3c65; }
    </style>
</head>
<body>
    <header>Studio Medico d'Élite — Dr. Diego Martinez</header>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono pronto ad analizzare referti, sintomi e terapie in tempo reale. Come posso aiutarti oggi?</div>
        {% if user_query %}
            <div class="message user">{{ user_query }}</div>
            <div class="message bot">{{ bot_response }}</div>
        {% endif %}
    </div>

    <div class="input-container">
        <form method="POST" style="display: flex; width: 100%; gap: 10px;">
            <textarea name="query" placeholder="Scrivi qui il tuo quesito clinico o incolla i referti..." required autofocus></textarea>
            <button type="submit">Invia</button>
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
        user_query = request.form.get("query")
        if user_query:
            try:
                chat = model.start_chat(history=[])
                response = chat.send_message(user_query)
                bot_response = response.text
            except Exception as e:
                bot_response = f"Errore di sincronizzazione neurale: {str(e)}"
    return render_template_string(HTML_PAGE, user_query=user_query, bot_response=bot_response)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
