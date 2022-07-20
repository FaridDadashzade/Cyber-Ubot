# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import requests
from googletrans import Translator
from telethon import events
from telethon.tl.types import User
from userbot import BLACKLIST_CHAT
from userbot import LOGS, bot, LANGUAGE as DIL
from userbot.events import register
from userbot.cmdhelp import CmdHelp

translator = Translator()
LANGUAGE = DIL

aktivet = []
LANGUAGES = "AZ"

url = "http://api.brainshop.ai/get?bid=168019&key=axrPMxmyHVdc37Sv&uid=cyberuserbot&msg={message}"

# ---------------------------------- #

from userbot.language import get_value
LANG = get_value("cyberlangs")

# ---------------------------------- #

async def cavablama(message):
    link = url.format(message=message)
    try:
        data = requests.get(link)
        if data.status_code == 200:
            return (data.json())["cnt"]
        LOGS.info("Xəta baş verdi!")
    except Exception:
        LOGS.info("Xəta: {str(e)}")


async def aktivetme(db, event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(LANG["PROHIBITED_COMMAND"])
    status = event.pattern_match.group(1).lower()
    chat_id = event.chat_id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            return await event.edit(LANG["CHATBOT_ACTIVE"])
        await event.edit(LANG["CHATBOT_DEACTIVE"])
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await event.edit(LANG["CHATBOT_DEACTIVE"])
        await event.edit(LANG["CHATBOT_DEACTIVE"])
    else:
        await event.edit(LANG["CHATBOT_MANUAL"])


@register(outgoing=True, disable_errors=True, pattern=r"^\.chatbot(?: |$)(.*)")
async def chatbot(event):
    await aktivetme(aktivet, event)


@register(incoming=True, disable_errors=True)
async def chatbot(event):
    sender = await event.get_sender()
    if not isinstance(sender, User):
        return
    if event.chat_id not in aktivet:
        return
    if event.text and event.is_reply:
        rep = await cavablama(event.message.message)
        tr = translator.translate(rep, LANGUAGE)
        if tr:
            await event.reply(tr.text) 

CmdHelp('chatbot').add_command(
'chatbot on', None, 'ChatBot modulunu aktiv edər.'
    ).add_command(
        'chatbot off', None, 'ChatBot modulunu deaktiv edər.'
    ).add()