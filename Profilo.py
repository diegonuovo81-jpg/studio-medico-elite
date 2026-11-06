try:
                if model is not None:
                    response = model.generate_content(user_query)
                    # Usiamo direttamente il testo estratto dalla IA in tempo reale
                    bot_response = response.text
                else:
                    bot_response = "Studio Medico d'Élite: Chiave API non rilevata dal sistema."
            except Exception as e:
                bot_response = f"Errore nell'elaborazione neurale: {str(e)}"
