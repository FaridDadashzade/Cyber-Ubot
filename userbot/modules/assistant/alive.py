# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import events
from telethon.events import *
from . import tgbot

ALIVE_LOGO = "https://telegra.ph/file/c3e75eccaeb7f56dfae89.mp4"
CYBER_VERSION = "3.0.0"
alive_text = "Cyber Asistanı aktivdir."

@tgbot.on(events.NewMessage(pattern="^/alive"))
async def alive(event):
    await tgbot.send_file(event.chat_id, ALIVE_LOGO, caption=alive_text)