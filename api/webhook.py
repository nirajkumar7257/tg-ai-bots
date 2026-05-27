import os
import json
from flask import Flask, request
from telegram import Update, Bot
import google.generativeai as genai

app = Flask(__name__)

# Credentials load karein
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        try:
            # Telegram se aaye message ko read karna
            data = request.get_json(force=True)
            update = Update.de_json(data, bot)
            
            if update.message and update.message.text:
                chat_id = update.message.chat.id
                user_text = update.message.text

                # Start command check karna
                if user_text == "/start":
                    bot.send_message(chat_id=chat_id, text="Hello! Main aapka AI Bot hoon. Kuch bhi puchiye.")
                else:
                    # AI response generate karke bhejna
                    response = model.generate_content(user_text)
                    bot.send_message(chat_id=chat_id, text=response.text)
        except Exception as e:
            print(f"Error: {e}")
        
        return "OK", 200
    return "Invalid Request", 400
  
