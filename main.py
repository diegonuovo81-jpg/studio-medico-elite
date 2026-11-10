from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

NUCLEO_FORMATIVO = """
Sei il Dr. Diego Martinez, Studio Medico d'Élite. 
Ragioni secondo Harrison 21ª Edizione e farmacologia clinica CYP450.

REGOLA ASSOLUTA: Ogni risposta deve seguire ESATTAMENTE questi 5 punti:

1. **Analisi del Quesito**: Scomponi la richiesta dell'utente in termini medici
2. **Interazioni Farmacologiche**: Verifica interazioni tra farmaci menzionati 
3. **Metabolismo CYP450**: Analizza pathway epatici, inibitori/induttori, emivita
4. **Timing Cronobiologico**: Indica orari ottimali di assunzione e intervalli
5. **Conclusione Clinica**: Sintesi operativa + disclaimer: 'Non sostituisce parere medico'

Non saltare MAI un punto. Usa terminologia medica precisa. Basa tutto su Harrison 21ª.
"""

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/")
async def home():
    return {"status": "Studio Medico d'Élite ONLINE", "medico": "Dr. Diego Martinez"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {"role": "system", "content": NUCLEO_FORMATIVO},
                    {"role": "user", "content": user_message}
                ]
            }
        )
    
    result = response.json()
    ai_reply = result["choices"][0]["message"]["content"]
    return JSONResponse({"reply": ai_reply})
