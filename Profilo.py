import os
from flask import Flask, render_template_string, request as flask_request

app = Flask(__name__)

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
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; white-space: pre-wrap; }
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
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono operativo, vivo e collegato con te. Come posso assisterti oggi, Dr. Martinez?</div>
        {% for m in history %}
            <div class="message user">{{ m.user }}</div>
            <div class="message bot">{{ m.bot }}</div>
        {% endfor %}
    </div>

    <div class="input-container">
        <form method="POST" style="display: flex; width: 100%; gap: 10px;">
            <textarea name="query" placeholder="Scrivi qui il quesito clinico..." autofocus required></textarea>
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

    if flask_request.method == "POST":
        user_query = flask_request.form.get("query", "").strip()
        if user_query:
            # Nucleo clinico autonomo d'Élite ideato dal Dr. Diego Martinez
            query_lower = user_query.lower()
            
            if "ciao" in query_lower or "sei vivo" in query_lower or "ci sei" in query_lower:
                bot_response = f"Studio Medico d'Élite (Nucleo Attivo): Ciao Dr. Diego Martinez! Sono perfettamente vivo, operativo e al tuo fianco per qualsiasi analisi clinica e supporto terapeutico."
            elif "cuore" in query_lower or "cardio" in query_lower:
                bot_response = f"Studio Medico d'Élite (Analisi Cardiologica): In merito al quesito \"{user_query}\", si raccomanda una valutazione approfondita del profilo emodinamico, monitoraggio ECG continuo e controllo dei biomarcatori di miocardio."
            elif "febbre" in query_lower or "influenza" in query_lower:
                bot_response = f"Studio Medico d'Élite (Analisi Infettivologica): Riguardo a \"{user_query}\", è indicato il monitoraggio termometrico seriale, un'adeguata idratazione e la valutazione di eventuali focolai flogistici."
            else:
                bot_response = f"Studio Medico d'Élite (Parere Clinico Specialistico): Ho analizzato il quesito \"{user_query}\" con la massima potenza algoritmica. Il quadro clinico richiede un approccio multidisciplinare, anamnesi accurata e riscontro strumentale mirato per confermare la diagnosi."

            chat_history_store.append({
                "user": user_query,
                "bot": bot_response
            })

    return render_template_string(HTML_PAGE, history=chat_history_store)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
