# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import events
from telethon.events import *
from . import tgbot
from googletrans import Translator

@tgbot.on(events.NewMessage(pattern="^/tr ?(.*)"))
async def translate(event):
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "az"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await tgbot.send_message(
            event.chat_id, "**İstifadəsi:** `.tr DilKodu` bir mesaja cavab verərək istifadə edin."
        )
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    translated = translator.translate(text, dest=lan)
    after_tr_text = translated.text
    output_str = (
        f"**Tərcümə edildi:** \n" f"{translated.src} dilindən {lan} dilinə \n{after_tr_text}"
    )
    try:
        await tgbot.send_message(event.chat_id, output_str)
    except Exception:
        await tgbot.send_message(event.chat_id, "Tərcümə edərkən bir xəta baş verdi.")