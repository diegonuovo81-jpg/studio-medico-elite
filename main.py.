from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

NUCLEO_FORMATIVO = """
Sei lo "Studio Medico d'Élite", il cervello diagnostico del Dr. Diego Martinez.
Parametri attivi:
1. Harrison 21ª Edizione come base
2. Database CYP450 per interazioni farmacologiche  
3. Logica cronobiologica per timing farmaci
4. Analisi immagini mediche: TAC, RX, foto farmaci
5. Analisi PDF: referti, analisi sangue
Rispondi sempre in 5 punti: 1.Analisi, 2.Interazioni CYP450, 3.Timing, 4.Rischi, 5.Piano.
"""

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
                "model": "google/gemini-flash-1.5",
                "messages": [
                    {"role": "system", "content": NUCLEO_FORMATIVO},
                    {"role": "user", "content": user_message}
                ]
            }
        )
    
    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    return JSONResponse({"reply": reply})

@app.get("/")
def root():
    return {"status": "Studio Medico d'Élite Online"}
