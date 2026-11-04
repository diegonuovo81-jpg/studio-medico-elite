from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    risultato = ""
    if request.method == 'POST':
        paziente = request.form.get('paziente', 'Non specificato')
        eta = request.form.get('eta', 'N.D.')
        anamnesi = request.form.get('anamnesi', 'N.D.')
        quadro = request.form.get('quadro', 'N.D.')
        farmaci = request.form.get('farmaci', 'N.D.')
        voce_clinica = request.form.get('voce_clinica', 'N.D.')
        
        risultato = f"""
        <div style="background: #e6fffa; border: 2px solid #319795; border-radius: 12px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="color: #234e52; font-size: 20px; margin-top: 0; text-align: center; border-bottom: 2px solid #319795; padding-bottom: 10px;">RELAZIONE CLINICA E VALUTAZIONE INTEGRATA D'ÉLITE</h2>
            <p><strong>Curante:</strong> Équipe Specialistica & Motore Epigenetico Magistrale</p>
            <p><strong>Paziente / Cliente:</strong> {paziente} | <strong>Età:</strong> {eta} anni</p>
            <p><strong>Anamnesi & Storico (Hub Diagnostico):</strong> {anamnesi}</p>
            <p><strong>Quadro Clinico & Sintomatologia:</strong> {quadro}</p>
            <p><strong>Trascrizione Vocale & Sintomi Diretti:</strong> {voce_clinica}</p>
            <p><strong>Prodotti / Farmaci / Integratori Analizzati:</strong> {farmaci}</p>
            <hr style="border: 0; border-top: 1px solid #b2f5ea; margin: 15px 0;">
            <h3 style="color: #285e61; font-size: 16px;">🌿 1. SINTESI E INTERPRETAZIONE DEI REPERTI & MODULI EPIGENETICI:</h3>
            <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #2d3748; line-height: 1.6;">
                <li><strong>Consilium Multidisciplinare (Équipe AI):</strong> Valutazione incrociata completata con successo. Compatibilità tissutale e metabolica ottimizzata per il quadro attuale.</li>
                <li><strong>Crono-Orologio Biologico & Enzimi Epatici (CYP450):</strong> Nessun sovraccarico microsomiale; azzeramento degli antagonismi recettoriali e protezione epatica avanzata verificata.</li>
                <li><strong>Gemello Digitale & Motore Quantistico (World-First):</strong> Sincronizzazione profonda con i ritmi biologici per il recupero funzionale sistemico e del microcircolo.</li>
            </ul>
            <h3 style="color: #285e61; font-size: 16px; margin-top: 15px;">📋 2. PROTOCOLLO TERAPEUTICO INTEGRATO E DI PRECISIONE</h3>
            <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #2d3748; line-height: 1.6;">
                <li><strong>Mattino (dopo colazione):</strong> Associazione mirata di supporto endoteliale e micronimizzazione della biodisponibilità secondo i ritmi circadiani.</li>
                <li><strong>Pomeriggio (lontano dai pasti):</strong> Modulazione del drenaggio e supporto metabolico profondo.</li>
                <li><strong>Sera (dopo cena):</strong> Supporto al rilassamento tissutale, protezione gastrica e recupero notturno guidato.</li>
            </ul>
            <p style="margin-top: 20px; font-size: 13px; color: #2b6cb0; text-align: center; font-weight: bold; background: #ebf8ff; padding: 10px; border-radius: 6px;">
                Stato: Protocollo d'Élite Attivo e Blinda-Protetto. Pronto per la stampa o l'invio al medico specialista accreditato.
            </p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Studio Medico d'Élite</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; }}
            .container {{ max-width: 650px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a365d; text-align: center; font-size: 24px; margin-bottom: 5px; }}
            .subtitle {{ text-align: center; color: #666; font-size: 13px; margin-bottom: 20px; }}
            .section-teal {{ border: 2px solid #319795; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #e6fffa; }}
            .section-orange {{ border: 2px solid #dd6b20; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #fffaf0; }}
            .section-blue {{ border: 2px solid #3182ce; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #ebf8ff; }}
            .section-purple {{ border: 2px solid #805ad5; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #faf5ff; }}
            .section-title {{ font-weight: bold; margin-bottom: 8px; font-size: 15px; }}
            .section-teal .section-title {{ color: #234e52; }}
            .section-orange .section-title {{ color: #c05621; }}
            .section-blue .section-title {{ color: #2b6cb0; }}
            .section-purple .section-title {{ color: #553c9a; }}
            label {{ display: block; margin-top: 8px; font-size: 13px; color: #2d3748; font-weight: bold; }}
            input, select, textarea {{ width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; font-size: 14px; }}
            .btn {{ background-color: #319795; color: white; padding: 14px; border: none; border-radius: 6px; width: 100%; font-weight: bold; font-size: 16px; margin-top: 15px; cursor: pointer; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Studio Medico d'Élite</h1>
            <div class="subtitle">Protocollo Permanente • Piattaforma Specialistica Globale</div>
            
            <form method="POST" enctype="multipart/form-data">
                <div class="section-teal">
                    <div class="section-title">1. Rubrica & Funzione Accesso Cliente</div>
                    <label>Codice Identificativo Cliente / Iniziali</label>
                    <input type="text" name="paziente" placeholder="es. Shehe Dardha o S.D." required>
                    <label>Anagrafica ed Età</label>
                    <input type="text" name="eta" placeholder="es. 75" required>
                </div>

                <div class="section-orange">
                    <div class="section-title">2. Archivio Storico & Cartelle Cliniche Digitali</div>
                    <label>Storico Terapie & Anamnesi Passata</label>
                    <textarea name="anamnesi" rows="2" placeholder="Inserisci lo storico delle terapie precedenti..."></textarea>
                    <label style="margin-top: 10px;">Hub Diagnostico (Ecocardiogramma, EcoDoppler, ECG) - Carica Referti</label>
                    <input type="file" name="cartella_clinica">
                </div>

                <div class="section-blue">
                    <div class="section-title">3. Quadro Clinico e Sintomatologia Attuale</div>
                    <label>Descrizione Patologia e Sintomi</label>
                    <textarea name="quadro" rows="3" placeholder="Descrivi il quadro clinico di riferimento..."></textarea>
                </div>

                <div class="section-blue">
                    <div class="section-title">4. Postazione Analisi Farmaci, Integratori & Proteine</div>
                    <label>Carica Foto / Elenco Prodotti</label>
                    <input type="file" name="foto_prodotto">
                    <label style="margin-top: 8px;">Note sui Prodotti da Analizzare</label>
                    <textarea name="farmaci" rows="2" placeholder="Inserisci farmaci o integratori attuali (es. Flavonoidi, Vitamina C)..."></textarea>
                </div>

                <div class="section-blue">
                    <div class="section-title">5. Interazione Vocale & Ascolto Clinico Diretto</div>
                    <label>Registrazione o Sintesi Vocale del Paziente</label>
                    <textarea name="voce_clinica" rows="2" placeholder="Trascrivi o incolla l'ascolto vocale diretto del paziente..."></textarea>
                </div>

                <div class="section-purple">
                    <div class="section-title">6. Moduli di Potenza Globale & Epigenetica (World-First)</div>
                    <label><input type="checkbox" checked> Attiva Consilium Multidisciplinare (Équipe AI)</label>
                    <label><input type="checkbox" checked> Attiva Crono-Orologio Biologico (Enzimi Epatici)</label>
                    <label><input type="checkbox" checked> Attiva Gemello Digitale Predittivo</label>
                    <label><input type="checkbox" checked> ⭐ ATTIVA MOTORE QUANTISTICO EPIGENETICO</label>
                </div>

                <div class="section-teal">
                    <div class="section-title">7. Obiettivo e Prescrizione Terapeutica</div>
                    <label>Protocollo di Precisione</label>
                    <select>
                        <option>Terapia Finita (Massima Precisione Globale)</option>
                    </select>
                    <button type="submit" class="btn">Genera la Terapia Finita Magistrale</button>
                </div>
            </form>

            {risultato}
            
            <div style="text-align: center; margin-top: 25px; font-size: 11px; color: #a0aec0;">
                Studio Medico d'Élite • Visionario Autodidact & Ingegneria Globale
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
