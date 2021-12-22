# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import events
from telethon.events import *
from . import tgbot, CYBER_VERSION, DEFAULT_NAME
from platform import python_version
from telethon import version

ALIVE_LOGO = "https://telegra.ph/file/c3e75eccaeb7f56dfae89.mp4"

alive_text = (
        f"**✦ C Y B Ξ R ASSISTANT ONLINE ✦** \n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━\n"
        f"┣[ ⛄️ **Sahibim:** `{DEFAULT_NAME}`\n"
        f"┣[ ❄️ **Python:** `{python_version()}`\n"                               
        f"┣[ ⛄️ **Telethon:** `{version.__version__}`\n"
        f"┣[ ☃️ **Branch:** `Master`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎄 **C Y B Ξ R Version:** `{CYBER_VERSION}`"
        )


@tgbot.on(events.NewMessage(pattern="^/start"))
async def alive(event):
    await tgbot.send_file(event.chat_id, ALIVE_LOGO, caption=alive_text)