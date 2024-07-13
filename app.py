import asyncio
from flask import Flask, render_template, request, jsonify
from characterai import aiocai
import os
import sys
import threading
import time

app = Flask(__name__)

#Ganti dengan token nya di https://old.character.ai/
API_TOKEN = 'YOUR_KEY'
client = aiocai.Client(API_TOKEN)
CHARACTER_ID = 'CHARACTER_ID'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    response = asyncio.run(chat_with_character(CHARACTER_ID, user_input))
    
    threading.Thread(target=restart_server).start()
    
    return jsonify(response)

async def chat_with_character(char_id, user_input):
    try:
        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(char_id, me.id)
            message = await chat.send_message(char_id, new.chat_id, user_input)
            return {'user_message': user_input, 'ai_message': message.text}
    except Exception as e:
        return {'user_message': user_input, 'ai_message': f"Error: {e}"}

def restart_server():
    import time
    time.sleep(1)
    python = sys.executable
    os.execl(python, f'"{python}"', *sys.argv)

if __name__ == '__main__':
    app.run(debug=True)
