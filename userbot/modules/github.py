# Copyright (C) 2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import json
import requests
from userbot.events import register
from userbot import CMD_HELP
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("github")

# ████████████████████████████████ #

@register(pattern=r".git (.*)", outgoing=True)
async def github(event):
    URL = requests.get(f"https://api.github.com/users/{event.pattern_match.group(1)}")
    chat = await event.get_chat()

    url = URL.json()['html_url']
    name = URL.json()['name']
    company = URL.json()['company']
    bio = URL.json()['bio']
    created_at = URL.json()['created_at']

    REPLY = f"`{event.pattern_match.group(1)} {LANG['INFO']}:`\
    \n{LANG['NAME']}: `{name}`\
    \nBio: `{bio}`\
    \nURL: {url}\
    \n{LANG['COMPANY']}: `{company}`\
    \n{LANG['CREATED']}: `{created_at}`"

    REPLY += f"\n{LANG['REPOS']}\n"

    await event.edit(REPLY) 
    

CmdHelp('git').add_command(
    'git', '<istifadəçi adı>', 'Seçilən istifadəçinin GitHub məlumatlarını göstərər.', 'git FaridDadashzade'
).add()