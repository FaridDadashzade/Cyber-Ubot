# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from userbot.cmdhelp import CmdHelp
from userbot import PLUGIN_CHANNEL_ID, CMD_HELP
from userbot.events import register
from re import search
from json import loads, JSONDecodeError
from userbot.language import LANGUAGE_JSON
from os import remove
import heroku3
import asyncio
import aiohttp
import ssl
import requests
from userbot.events import register 
from userbot.cmdhelp import CmdHelp
from userbot import HEROKU_APIKEY, HEROKU_APPNAME 
from shutil import which

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None

DIL_SIYAHISI = ["AZ", "TR", "EN", "IN", "UZ"]

@register(outgoing=True, pattern="^.dil ?(.*)")
async def dil(event):
    global LANGUAGE_JSON

    komut = event.pattern_match.group(1)
    if search(r"y[uü]kl[eə]|install", komut):
        await event.edit("`Dil faylı yüklənir...`")
        if event.is_reply:
            reply = await event.get_reply_message()
            dosya = await reply.download_media()

            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "cyberjson")):
                return await event.edit("`Xahiş edirəm bir` **CYBERJSON** `faylına cavab verin!`")

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xahiş edirəm bir` **CYBERJSON** `faylına cavab verin!`")

            await event.edit(f"`{dosya['LANGUAGE']}` `dili yüklənir...`")
            pchannel = await event.client.get_entity(PLUGIN_CHANNEL_ID)

            dosya = await reply.download_media(file="./userbot/language/")
            dosya = loads(open(dosya, "r").read())
            await reply.forward_to(pchannel)
            
            LANGUAGE_JSON = dosya
            await event.edit(f"✅ `{dosya['LANGUAGE']}` `dili uğurla yükləndi!`")
        else:
            await event.edit("**Xahiş edirəm bir dil faylına cavab verin.**")
    elif search(r"melumat|info", komut):
        await event.edit("`Dil faylı haqqında məlumatlar gətirilir.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "cyberjson")):
                return await event.edit("`Xahiş edirəm bir` **CYBERJSON** `faylına cavab verin!`")

            dosya = await reply.download_media()

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xahiş edirəm bir` **CYBERJSON** `faylına cavab verin!`")

            await event.edit(
                f"**Dil: **`{dosya['LANGUAGE']}`\n"
                f"**Dil kodu: **`{dosya['LANGCODE']}`\n"
                f"**Tərcümə edən: **`{dosya['AUTHOR']}`\n"

                f"\n\n`Dil faylını yükləmək üçün` `.lang install` `yazın`"
            )
        else:
            await event.edit("**Xahiş edirəm bir dil faylına cavab verin!**")
    else:
        await event.edit(
            f"**Dil: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Dil kodu: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Tərcümə edən: **`{LANGUAGE_JSON ['AUTHOR']}`\n"

            f"\n\n**C Y B Ξ R USERBOT**"
        )

# The codes belong entirely to https://github.com/FaridDadashzade. Reuse is not allowed.
# Başqa botlarda istifadəsi qadağandır!
# © https://t.me/FVREED 

@register(cyber=True, pattern="^.dil deyis ?(.*)")
@register(cyber=True, pattern="^.dil değiş ?(.*)")
async def dil_deyis(cyber):
    dil_adi = cyber.pattern_match.group(1)
    if not dil_adi in DIL_SIYAHISI: # yazdiginiz dil adi dil siyahisinda yoxdursa return
        await cyber.edit("**Xahiş edirəm düzgün bir dil adı qeyd edin!**\n**Dil siyahısı:** `AZ, TR, EN, IN, UZ`")
        return
    if dil_adi == '': # dil adi qeyd olunmayibsa return
        await cyber.edit("**Xahiş edirəm düzgün bir dil adı qeyd edin!**\n**Dil siyahısı:** `AZ, TR, EN, IN, UZ`")
        return
    await cyber.edit(f"**Botunuzun dili** `{dil_adi}` **olaraq ayarlandı!**")
    try:
        heroku_var["LANGUAGE"] = dil_adi
    except:
        await cyber.edit("`Dil dəyişdirmə prosesi zamanı xəta baş verdi!`")

# The codes belong entirely to https://github.com/FaridDadashzade. Reuse is not allowed.
# Başqa botlarda istifadəsi qadağandır!
# © https://t.me/FVREED 

CmdHelp('dil').add_command(
    'dil', None, 'Yüklədiyiniz dil haqqında məlumat verər.'
).add_command(
    'dil info', None, 'Cavab verdiyiniz dil faylı haqqında məlumat verər.'
).add_command(
    'dil install', None, 'Cavab verdiyiniz dil faylını yükləyər.'
).add_command(
    'dil deyis', None, 'Botunuzun dilini dəyişdirər.' 
).add()
