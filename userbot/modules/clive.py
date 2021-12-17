# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import asyncio
from telethon import events
from userbot import SUDO_ID, SUDO_VERSION, CYBER_VERSION
from userbot.cmdhelp import CmdHelp
from userbot.events import register

@register(sudo=True, pattern="^.calive$")
async def sudoers(s):
    await s.client.send_message(s.chat_id,f"`C Y B Ξ R USERBOT\nSudo aktivdir...\nC Y B Ξ R Version: {CYBER_VERSION}\nSudo Version: {SUDO_VERSION}`")
    
Help = CmdHelp('calive')
Help.add_command('calive', None, 'Sudo aktiv olub olmadığını yoxlamaq üçün.')
Help.add()
