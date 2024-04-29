import io
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

API_TOKEN = os.getenv("TOKEN")
REMOVE_BG_API_KEY = os.getenv("RMBG")

def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
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

    help_button = InlineKeyboardButton("𝖧𝖾𝗅𝗉", callback_data='help')
    keyboard.row(help_button)

    update.message.reply_text(message_text, reply_markup=keyboard)

def remove_background(update: Update, context: CallbackContext) -> None:
    message = update.message
    chat_id = message.chat_id

    if message.photo:
        file_id = message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        downloaded_file = file.download_as_bytearray()

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': ('input.png', io.BytesIO(downloaded_file), 'image/png')},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG_API_KEY},
        )

        if response.status_code == 200:
            context.bot.send_photo(chat_id=chat_id, photo=response.content)
        else:
            update.message.reply_text('Error processing image. Please try again.')

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'about':
        query.edit_message_text(text="𝖡𝗈𝗍 : Backround Remover Bot\n"
                                      "𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 : [GitHub] (https://github.com/Geektyper) | [Telegram] (https://telegram.me/NotRealGeek)\n"
                                      "𝖲𝗈𝗎𝗋𝖼𝖾 : [Click here] (https://github.com/Geektyper/background)\n"
                                      "𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 : [Python 3] (https://python.org/)\n"
                                      "𝖫𝗂𝖻 : Pyrogram (https://pyrogram.org/)")
    elif query.data == 'close':
        query.edit_message_text(text="𝖢𝗅𝗈𝗌𝖾𝖽")
    elif query.data == 'help':
        buttons = [
            [
                InlineKeyboardButton("Close", callback_data='close_help')
            ]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        query.edit_message_text(text="Just send me a photo\n"
                                      "- I will download it\n"
                                      "- I will send the photo without background\n"
                                      "Made by [Geektyper](t.me/notrealgeek).",
                                reply_markup=keyboard)

def main() -> None:
    updater = Updater(token=API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, remove_background))
    dispatcher.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()