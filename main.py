import io
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = os.getenv("TOKEN")
REMOVE_BG_API_KEY = os.getenv("RMBG")

app = Client("my_bot", bot_token=API_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    user_name = message.from_user.first_name
    message_text = (
        f"𝖧ey {user_name}, 𝖨 𝖠𝗆 𝖠 𝖬𝖾𝖽𝗂𝖺 𝖡𝖺𝖼𝗄𝗀𝗋𝗈𝗎𝗇𝖽 𝖱𝖾𝗆𝗈𝗏𝖾𝗋 𝖡𝗈𝗍!\n\n"
        "𝖲𝖾𝗇𝖽 𝖬𝖾 𝖠 𝖯𝗁𝗈𝗍𝗈 𝖨 𝖶𝗂𝗅𝗅 𝖲𝖾𝗇𝖽 𝖳𝗁𝖾 𝖯𝗁𝗈𝗍𝗈 𝖶𝗂𝗍𝗁𝗈𝗎𝗍 𝖡𝖺𝖼𝗄𝗀𝗋𝗈𝗎𝗇𝖽!"
    )

    buttons = [
        [
            InlineKeyboardButton("𝖠𝖻𝗈𝗎𝗍", callback_data='about'),
            InlineKeyboardButton("𝖢𝗅𝗈𝗌𝖾", callback_data='close')
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    message.reply_text(message_text, reply_markup=keyboard)

@app.on_message(filters.photo)
def remove_background(client, message):
    chat_id = message.chat.id

    if message.photo:
        file_id = message.photo[-1].file_id
        file = client.download_media(file_id)
        file_io = io.BytesIO(file)

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': ('input.png', file_io, 'image/png')},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG_API_KEY},
        )

        if response.status_code == 200:
            client.send_photo(chat_id=chat_id, photo=response.content)
        else:
            message.reply_text('Error processing image. Please try again.')

@app.on_callback_query()
def button_click(client, callback_query):
    query = callback_query
    query.answer()
    if query.data == 'about':
        query.edit_message_text(text="𝖡𝗈𝗍 : Backround Remover Bot\n"
                                      "𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 : GitHub (https://github.com/Geektyper) | Telegram (https://telegram.me/NotRealGeek)\n"
                                      "𝖲𝗈𝗎𝗋𝖼𝖾 : Click here (https://github.com/Geektyper/background)\n"
                                      "𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 : Python 3 (https://python.org/)\n"
                                      "𝖫𝗂𝖻 : Pyrogram (https://pyrogram.org/)")
    elif query.data == 'close':
        query.edit_message_text(text="𝖢𝗅𝗈𝗌𝖾𝖽")

if __name__ == '__main__':
    app.run()