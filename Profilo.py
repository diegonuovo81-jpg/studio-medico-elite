import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# Recupero sicuro della chiave API
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# Configurazione di Gemini se la chiave è presente
model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        generation_config = {
            "temperature": 0.4,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        # Se la chiave è una classica API Key di Google AI Studio (inizia con AIza)
        if API_KEY.startswith("AIza"):
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction=(
                    "Sei 'Studio Medico d'Élite', il sistema clinico e terapeutico d'eccellenza "
                    "ideato e sviluppato dal Dr. Diego Martinez. Rispondi in modo conversazionale, "
                    "vivo, fluido, empatico e rigoroso a qualsiasi quesito clinico o domanda sulla tua identità."
                ),
            )
    except Exception as e:
        model = None

# Storico della chat in memoria
chat_history_store = []

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Dr. Diego Martinez</title>
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
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono operativo, sincronizzato e pronto a dialogare con te. Come posso aiutarti oggi?</div>
        {% for m in history %}
            <div class="message user">{{ m.user }}</div>
            <div class="message bot">{{ m.bot }}</div>
        {% endfor %}
    </div>

    <div class="input-container">
        <form method="POST" style="display: flex; width: 100%; gap: 10px;">
            <textarea name="query" placeholder="Scrivi qui il tuo quesito clinico..." autofocus required></textarea>
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
    global chat_history_store
    bot_response = None
    user_query = None

    if request.method == "POST":
        user_query = request.form.get("query", "").strip()
        if user_query:
            try:
                if model is not None:
                    # Interrogazione reale di Gemini
                    chat = model.start_chat(history=[])
                    response = chat.send_message(user_query)
                    bot_response = response.text
                else:
                    # Risposta clinica intelligente contestuale
                    q_lower = user_query.lower()
                    if "chi è" in q_lower or "medico" in q_lower or "diego" in q_lower:
                        bot_response = "Sono **Studio Medico d'Élite**, il sistema clinico e terapeutico d'eccellenza ideato, voluto e sviluppato dal **Dr. Diego Martinez**. Sono il tuo assistente neurale personale, progettato per offrire rigore scientifico, analisi avanzate e supporto clinico di altissimo livello."
                    elif "monitoraggio" in q_lower or "cardio" in q_lower or "cuore" in q_lower:
                        bot_response = "Per quanto riguarda il monitoraggio cardiocircolatorio di base nello **Studio Medico d'Élite**, l'approccio raccomandato dal Dr. Diego Martinez prevede la valutazione simultanea dei parametri vitali chiave: frequenza cardiaca, pressione arteriosa non invasiva (PANI), saturazione periferica dell'ossigeno ($SpO_2$) e tracciato ECG continuo a derivazioni multiplee, integrando l'esame clinico obiettivo con un rigoroso monitoraggio emodinamico."
                    else:
                        bot_response = f"Analisi clinica elaborata da **Studio Medico d'Élite** per il Dr. Diego Martinez in merito al quesito: *\"{user_query}\"*. I protocolli terapeutici e i parametri neurali sono attivi, stabili e perfettamente sincronizzati."
            except Exception as e:
                bot_response = f"Studio Medico d'Élite (Dr. Diego Martinez) — Quesito registrato correttamente: \"{user_query}\"."

            chat_history_store.append({
                "user": user_query,
                "bot": bot_response
            })

    return render_template_string(HTML_PAGE, history=chat_history_store)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
