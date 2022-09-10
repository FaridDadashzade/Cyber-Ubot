# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import asyncio
import sys
import os
import time
from telethon.tl import functions
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)

from userbot import CMD_HELP, ASYNC_POOL, bot, DEFAULT_NAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("auto")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.auto ?(.*)")
async def auto(event):
    metod = event.pattern_match.group(1).lower()
    
    if str(metod) not in ("ad", "bio"):
        await event.edit(LANG['INVALID_TYPE'])
        return

    if metod in ASYNC_POOL:
        await event.edit(LANG['ALREADY'] % metod)
        return

    await event.edit(LANG['SETTING'] % metod)
    if metod == "ad":
        HM = time.strftime("%H:%M")

        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=LANG['NAME'] % HM
        ))
    elif metod == "bio":
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M")

        Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK'] 
        await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=Bio
        ))


    await event.edit(LANG['SETTED'] % metod)

    ASYNC_POOL.append(metod)

    while metod in ASYNC_POOL:
        try:
            if metod == "ad":
                HM = time.strftime("%H:%M")

                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    last_name=LANG['NAME'] % HM
                ))
            elif metod == "bio":
                DMY = time.strftime("%d.%m.%Y")
                HM = time.strftime("%H:%M")

                Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK'] 
                await event.client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=Bio
                ))

            await asyncio.sleep(60)
        except:
            return

        
@register(outgoing=True, pattern="^.resauto")
async def reauto(resauto):
    cyberad = DEFAULT_NAME
    about = DEFAULT_BIO
    if " " not in cyberad:
        firstname = cyberad
        lastname = ""
        about = about
    try:
      await resauto.client(UpdateProfileRequest(first_name=firstname, last_name=lastname, about=about))
      await resauto.edit("`Hesabınız uğurla əvvəlki halına qaytarıldı.`")
      await bot.disconnect()
      os.execl(sys.executable, sys.executable, *sys.argv)
    except: 
      pass

Help = CmdHelp('auto')
Help.add_command('auto', 'ad ya da bio', 'Avtomatik saata görə dəyişdirər', 'auto ad')
Help.add_command('resauto', None, 'Hesabınızı əvvəlki halına qaytarar', 'resauto')
Help.add()
