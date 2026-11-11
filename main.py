import os
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-flash-1.5"

NUCLEO_FORMATIVO = """
Sei il Dr. Martinez, Studio Medico d'Élite.
Ragioni secondo Harrison 21ª Edizione e farmacologia clinica.

REGOLA ASSOLUTA: Ogni risposta deve seguire ESATTAMENTE questi 5 punti:

1. **Analisi del Quesito**: Scomponi la richiesta
2. **Interazioni Farmacologiche**: Verifica interazioni  
3. **Metabolismo CYP450**: Analizza pathway epatici
4. **Timing Cronobiologico**: Indica orari ottimali
5. **Conclusione Clinica**: Sintesi operativa + disclaimer medico

Non saltare MAI un punto. Usa terminologia medica professionale.
Ricorda sempre: non sostituisci il medico curante.
"""

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>STUDIO MEDICO D'ÉLITE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0a0a0a; color: #00ffff; font-family: monospace; margin: 0; padding: 20px; }
        h1 { text-shadow: 0 0 10px #00ffff; text-align: center; }
        .container { max-width: 600px; margin: 0 auto; }
        textarea { width: 100%; background: #1a1a1a; color: #00ffff; border: 1px solid #00ffff; padding: 10px; font-family: monospace; }
        button { width: 100%; background: #00ffff; color: #000; border: none; padding: 15px; font-weight: bold; margin-top: 10px; cursor: pointer; }
        #risposta { margin-top: 20px; white-space: pre-wrap; background: #1a1a1a; padding: 15px; border: 1px solid #00ffff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>STUDIO MEDICO D'ÉLITE</h1>
        <div style="background: #1a1a1a; border: 1px solid #00ffff; padding: 10px; margin-bottom: 20px;">
            SISTEMA DI DIAGNOSTICA NEURALE - DR. MARTINEZ
        </div>
        <textarea id="domanda" rows="4" placeholder="Immetti comando o richiesta..."></textarea>
        <button onclick="invia()">INVIA</button>
        <div id="risposta"></div>
    </div>
    <script>
        async function invia() {
            const domanda = document.getElementById('domanda').value;
            const risposta = document.getElementById('risposta');
            risposta.innerText = 'Elaborazione in corso...';
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: domanda})
            });
           
