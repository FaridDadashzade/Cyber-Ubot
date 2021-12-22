# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import events
from userbot import *
from . import *
from userbot import ALIVE_LOGO, CYBER_VERSION, tgbot

alive_text = f"⚜ CYBER ONLINE ⚜ \n\n"
alive_text += f"Sahibim:『{CYBER_MENTION}』\n"
alive_text += f"**╭───────────**\n"
alive_text += f"┣Ťêlethon ~ `1.24.0` \n"
alive_text += f"┣ Cyber Version: `{CYBER_VERSION}` \n"
alive_text += f"╰────────────\n"
alive_text += f"       »»» [『 CYBER 』](https://t.me/TheCyberUserBot) «««"


@tgbot.on(events.NewMessage(pattern="^/alive"))
async def alive(event):
    await tgbot.send_file(event.chat_id, ALIVE_LOGO, caption=alive_text)