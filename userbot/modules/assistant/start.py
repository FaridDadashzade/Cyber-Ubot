# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon import events
from telethon.events import *
from . import tgbot, CYBER_VERSION, DEFAULT_NAME
from platform import python_version
from telethon import version

ALIVE_LOGO = "https://telegra.ph/file/c3e75eccaeb7f56dfae89.mp4"

HELP_LOGO = "https://telegra.ph/file/c3e75eccaeb7f56dfae89.mp4"

alive_text = (
        f"**✦ C Y B Ξ R ASSISTANT ONLINE ✦** \n"
        f"┏━━━━━━━━━━━━━━━━━━━━\n"
        f"┣[ 👤 **Sahibim:** `{DEFAULT_NAME}`\n"
        f"┣[ 🐍 **Python:** `{python_version()}`\n"                               
        f"┣[ ⚙️ **Telethon:** `{version.__version__}`\n"
        f"┣[ 🗄 **Branch:** `Master`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━\n"
        f"**Ətraflı məlumat üçün /help yazın.**"
        )

help_text = (
        f"**✦ C Y B Ξ R ASSISTANT HELP MENU ✦** \n"
        f"┏━━━━━━━━━━━━━━━━━━━━\n"
        f"┣[ `/start` - **Start mesajını göndərər.**\n"
        f"┣[ `/id` - **Bir qrup və ya istifadəçi ID almaq üçün.**\n"                               
        f"┣[ `/tr` - **Tərcümə edər.**\n"
        f"┣[ `/help` - **Bu mesajı atar.**\n"
        f"┣[ `/purge` - **Qeyd etdiyiniz mesajdan sonraki mesajları təmizləyər.**\n"
        f"┣[ `/del` - **Cavab verdiyiniz mesajı silər.**\n"
        f"┣[ `/ban` - **Bir istifadəçini ban etmək üçün.**\n"
        f"┣[ `/unban` - **Bir istifadəçinin banını açar.**\n"
        f"┣[ `/promote` - **Bir istifadəçini admin etmək üçün.**\n"
        f"┣[ `/demote` - **Bir istifadəçinin adminlik hüququnu almaq üçün.**\n"
        f"┣[ `/pin` - **Cavab verdiyiniz mesajı sabitləyər.**\n"
        f"┣[ `/lyrics` - **Adını yazdığınız musiqinin sözlərini axtarar.**\n"
        f"┗━━━━━━━━━━━━━━━━━━━━\n"
        )

@tgbot.on(events.NewMessage(pattern="^/start"))
async def start_cyber_bot(event):
    await tgbot.send_file(event.chat_id, ALIVE_LOGO, caption=alive_text)


@tgbot.on(events.NewMessage(pattern="^/help"))
async def help(event):
    await tgbot.send_file(event.chat_id, HELP_LOGO, caption=help_text)