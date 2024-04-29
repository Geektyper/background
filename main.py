import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = os.environ.get("RMBG")
IMG_PATH = "./DOWNLOADS"

Geek = Client(
    "RemoveBackgroundBot",
    bot_token=os.environ.get("TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
)


async def synchronize_time():
    await Geek.start()
    await Geek.get_me()
    await Geek.stop()


async def main():
    await synchronize_time()


if __name__ == "__main__":
    Geek.loop.run_until_complete(main())


START_TEXT = """
Hello {}, I am an image background remover bot. Send me a photo, and I will send the photo without background.

Made by [Bot support](t.me/BotsupportXD).
"""
HELP_TEXT = """
- Just send me a photo
- I will download it
- I will send the photo without background

Made by [Bot support](t.me/BotsupportXD).
"""
ABOUT_TEXT = """
- **Bot:** `Background Remover Bot`
- **Creator:** [Pratham](https://t.me/Notrealgeek)
- **Channel:** [Bot Updates](https://t.me/Botupdatexd)
- **Support:** [Bot support](https://t.me/BotsupportXD)
"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Updates', url='https://telegram.me/Botupdatexd'),
            InlineKeyboardButton('Support', url='https://telegram.me/Botupdatexd')
        ],
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ERROR_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)


@Geek.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Geek.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Geek.on_message(filters.private & (filters.photo | filters.document))
async def remove_background(bot, update):
    if not API:
        await update.reply_text(
            text="Error: Remove BG API is not available",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return

    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Analyzing...",
        quote=True,
        disable_web_page_preview=True
    )

    if update and update.media and (update.photo or (update.document and "image" in update.document.mime_type)):
        file_name = f"{IMG_PATH}/{update.from_user.id}/image.jpg"
        new_file_name = f"{IMG_PATH}/{update.from_user.id}/no_bg.png"

        await update.download(file_name)

        await message.edit_text(
            text="Photo downloaded successfully. Now removing background...",
            disable_web_page_preview=True
        )

        try:
            new_image = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": open(file_name, "rb")},
                data={"size": "auto"},
                headers={"X-Api-Key": API}
            )

            if new_image.status_code == 200:
                with open(new_file_name, "wb") as image:
                    image.write(new_image.content)
            else:
                await update.reply_text(
                    text="Error: API request failed",
                    quote=True,
                    reply_markup=ERROR_BUTTONS
                )
                return

            await update.reply_chat_action("upload_photo")
            await update.reply_document(
                document=new_file_name,
                quote=True
            )

            await message.delete()

            try:
                os.remove(file_name)
            except Exception as e:
                print(f"Error while deleting file: {e}")

        except Exception as error:
            print(f"Error: {error}")
            await message.edit_text(
                text="Something went wrong! Please try again later.",
                disable_web_page_preview=True,
                reply_markup=ERROR_BUTTONS
            )
    else:
        await message.edit_text(
            text="Media not supported",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )


if __name__ == "__main__":
    Geek.run()