export GEMINI_API_KEY="TUA_CHIAVE_API"
pip install -U google-genai
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Spiega come funziona l'IA in poche parole"
)
print(interaction.output_text)
from google import genai

client = genai.Client()

stream = client.interactions.create(
    model="gemini-3.8-flash",
    input="Spiega come funziona l'IA",
    stream=True
)
for event in stream:
    print(event)
    from google import genai

client = genai.Client()

interaction1 = client.interactions.create(
    model="gemini-3.8-flash",
    input="Ho 2 cani in casa.",
)
print("Risposta 1:", interaction1.output_text)

interaction2 = client.interactions.create(
    model="gemini-3.8-flash",
    input="Quante zampe ci sono in casa mia?",
    previous_interaction_id=interaction1.id,
)
print("Risposta 2:", interaction2.output_text)
import base64
from google import genai

client = genai.Client()

# Carica un'immagine locale
with open("sample.jpg", "rb") as f:
    image_bytes = f.read()
image_b64 = base64.b64encode(image_bytes).decode("utf-8")

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {"type": "text", "text": "Confronta questa immagine locale e questo file audio remoto."},
        {
            "type": "image",
            "data": image_b64,
            "mime_type": "image/jpeg"
        },
        {
            "type": "audio",
            "uri": "https://storage.googleapis.com/generativeai-downloads/data/sample.mp3",
            "mime_type": "audio/mp3"
        }
    ]
)
print(interaction.output_text)
import json
from google import genai

client = genai.Client()

weather_tool = {
    "type": "function",
    "name": "get_current_temperature",
    "description": "Ottiene la temperatura attuale per una determinata località.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "Il nome della città, es. Londra",
            },
        },
        "required": ["location"],
    },
}

available_functions = {
    "get_current_temperature": lambda location: {
        "location": location, "temperature": "22", "unit": "celsius"
    },
}

user_input = "Qual è la temperatura a Londra?"
previous_id = None

while True:
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=user_input,
        tools=[weather_tool],
        previous_interaction_id=previous_id,
    )

    function_results = []
    for step in interaction.steps:
        if step.type == "function_call":
            result = available_functions[step.name](**step.arguments)
            print(f"Chiamata a {step.name}({step.arguments}) → {result}")
            function_results.append({
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            })

    if not function_results:
        break

    user_input = function_results
    previous_id = interaction.id

print(interaction.output_text)
import time
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Scrivi un'analisi dettagliata sull'impatto dell'intelligenza artificiale nella sanità moderna.",
    background=True,
)
print(f"Attività in background avviata: {interaction.id}")

# Controllo dello stato (Polling)
while True:
    result = client.interactions.get(interaction.id)
    print(f"Stato: {result.status}")
    if result.status == "completed":
        print(f"\nRisultato:\n{result.output_text}")
        break
    elif result.status == "failed":
        print(f"Fallito: {result.error}")
        break
    time.sleep(5)
