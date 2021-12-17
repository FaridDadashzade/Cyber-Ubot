# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import os
import sys
from telethon.tl.types import DocumentAttributeFilename, InputMessagesFilterDocument
import importlib
import asyncio
import re
import time
from pathlib import Path
from os.path import exists
import traceback

from userbot import CMD_HELP, bot, tgbot, PLUGIN_CHANNEL_ID, PATTERNS, BOTLOG, BOTLOG_CHATID, DANGERCONFIGS, MYID, JARVIS
from userbot.events import register
from userbot.main import extractCommands
import userbot.cmdhelp
import base64

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__plugin")
LANG2 =  get_value("misc")

# ████████████████████████████████ #

# Plugin Porter - UniBorg
@register(cyber=True, pattern="^.pport")
async def pport(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        skanet = await yoxla(reply_message)
    else:
        await event.edit(LANG["REPLY_FOR_PORT"])
        return

    await event.edit(LANG["DOWNLOADING"])
    dosya = await event.client.download_media(reply_message)
    dosy = open(dosya, "r").read()

    borg1 = r"(@borg\.on\(admin_cmd\(pattern=\")(.*)(\")(\)\))"
    borg2 = r"(@borg\.on\(admin_cmd\(pattern=r\")(.*)(\")(\)\))"
    borg3 = r"(@borg\.on\(admin_cmd\(\")(.*)(\")(\)\))"

    if re.search(borg1, dosy):
        await event.edit(LANG["UNIBORG"])
        komu = re.findall(borg1, dosy)

        if len(komu) > 1:
            await event.edit(LANG["TOO_MANY_PLUGIN"])

        komut = komu[0][1]
        degistir = dosy.replace('@borg.on(admin_cmd(pattern="' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut + "(event):")
        degistir = degistir.replace("borg.", "event.client.")
        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit(LANG["UPLOADING"])

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")
    elif re.search(borg2, dosy):
        await event.edit(LANG["UNIBORG2"])
        komu = re.findall(borg2, dosy)

        if len(komu) > 1:
            await event.edit(LANG["TOO_MANY_PLUGIN"])
            return

        komut = komu[0][1]

        degistir = dosy.replace('@borg.on(admin_cmd(pattern=r"' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut + "(event):")
        degistir = degistir.replace("borg.", "event.client.")
        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit(LANG["UPLOADING"])

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")
    elif re.search(borg3, dosy):
        await event.edit(LANG["UNIBORG3"])
        komu = re.findall(borg3, dosy)

        if len(komu) > 1:
            await event.edit(LANG["TOO_MANY_PLUGIN"])
            return

        komut = komu[0][1]

        degistir = dosy.replace('@borg.on(admin_cmd("' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut.replace("?(.*)", "") + "(event):")
        degistir = degistir.replace("borg.", "event.client.")

        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit(LANG["UPLOADING"])

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")

    else:
        await event.edit(LANG["UNIBORG_NOT_FOUND"])

@register(outgoing=True, pattern="^.plist")
async def plist(event):
    if PLUGIN_CHANNEL_ID is not None:
        await event.edit(LANG["PLIST_CHECKING"])
        yuklenen = f"{LANG['PLIST']}\n\n"
        async for plugin in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument):
            try:
                dosyaismi = plugin.file.name.split(".")[1]
            except:
                continue

            if dosyaismi == "py":
                yuklenen += f"☑ {plugin.file.name}\n"
        await event.edit(yuklenen)
    else:
        await event.edit(LANG["TEMP_PLUGIN"])           

       
# bu modul CYBERUSERBOT-a özəl olaraq hazırlanmışdır yəniki
# oğurlama atanın balası
# modülü çalma peyser NSJDKFNDKDNKFKD

@register(cyber=True, pattern="^.pinstall")
async def _(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
    else:
        await event.edit(LANG["REPLY_TO_FILE"])
        return
    plugin_adi = reply_message.file.name
    cyber_path = f"userbot/modules/{plugin_adi}"
    uzanti = plugin_adi.split(".")[1].lower()
    plugin_exe = plugin_adi.split(".")[0]
    if uzanti != "py":
        await event.edit("`Xahiş edirəm bir Python faylına cavab verin!`")
        return
    if os.path.isfile(cyber_path):
        await event.edit("🎄 `Bu plugin onsuzda yüklənib!\nOnu təkrar yükləməyəcəyəm.`")
        return
    b = await event.client.download_media(await event.get_reply_message()) 
    a = open(b, "r") 
    c = a.read() 
    a.close() 
    a = await event.edit("`Plugin skan edilir...`\n`Biraz gözləyin...` 🎄") 
    for CYBER in DANGERCONFIGS:
      if re.search(CYBER, c):
        await event.edit(f"`Plugində` **{CYBER}** `dəyəri aşkar edildi!`\n`Plugin təhlükəli olduğundan onu sildim.`")
        return os.remove(b)
    else:
     await event.edit(LANG["DOWNLOADING"])
 
        
    dosyaAdi = reply_message.file.name

    dosya = await event.client.download_media(reply_message, "./userbot/modules/")

    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"{LANG['PLUGIN_BUGGED']} {e}")
        return os.remove("./userbot/modules/" + dosya)

    dosy = open(dosya, "r").read()
    if re.search(r"@tgbot\.on\(.*pattern=(r|)\".*\".*\)", dosy):
        komu = re.findall(r"\(.*pattern=(r|)\"(.*)\".*\)", dosy)
        komutlar = ""
        i = 0
        while i < len(komu):
            komut = komu[i][1]
            CMD_HELP["tgbot_" + komut] = f"{LANG['PLUGIN_DESC']} {komut}"
            komutlar += komut + " "
            i += 1
        await event.edit(LANG['PLUGIN_DOWNLOADED'] % komutlar)
    else:
        Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", dosy)

        if (not type(Pattern) is list) or (len(Pattern) < 1 or len(Pattern[0]) < 1):
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await reply_message.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'🎄 **Plugin uğurla yükləndi!**\n\n☃️ **Pluginin istifadəsini öyrənmək üçün** `.cyber {cmdhelp}` **yazın.**')
            else:
                await reply_message.forward_to(PLUGIN_CHANNEL_ID)
                userbot.cmdhelp.CmdHelp(dosya).add_warning('Əmr tapılmadı').add()
                return await event.edit(LANG['PLUGIN_DESCLESS'])
        else:
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await reply_message.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'🎄 **Plugin uğurla yükləndi!**\n\n☃️ **Pluginin istifadəsini öyrənmək üçün** `.cyber {cmdhelp}` **yazın.**')
            else:
                dosyaAdi = reply_message.file.name.replace('.py', '')
                extractCommands(dosya)
                await reply_message.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'🎄 **Plugin uğurla yükləndi!**\n\n☃️ **Pluginin istifadəsini öyrənmək üçün** `.cyber {dosyaAdi}` **yazın.**')
            
                         
                         
@register(cyber=True, pattern="^.premove ?(.*)")
async def premove(event):
    modul = event.pattern_match.group(1).lower()
    if len(modul) < 1:
        await event.edit(LANG['PREMOVE_GIVE_NAME'])
        return

    await event.edit(LANG['PREMOVE_DELETING'])
    a = 0
    r = 0
    async for message in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument, search=modul):
        await message.delete()
        try:
            os.remove(f"./userbot/modules/{message.file.name}")
            r +=1
        except FileNotFoundError:
            if r>1:
                pass
            else:
                await event.reply(LANG['ALREADY_DELETED'])


    if r == 0:
        await event.edit(LANG['NOT_FOUND_PLUGIN'])
    else:
        await event.edit(LANG['PLUG_DELETED'])
        time.sleep(2) 
        await event.edit(LANG2['RESTARTING'])
        try: 
            if BOTLOG:
                try:
                    await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                            "Plugin silindikdən sonra avtomatik restart prosesi tamamlandı.")
                except:
                    pass
            await bot.disconnect()
        except:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)

@register(cyber=True, pattern="^.psend ?(.*)")
async def psend(event):
    modul = event.pattern_match.group(1)
    if len(modul) < 1:
        await event.edit(LANG['PREMOVE_GIVE_NAME'])
        return

    if os.path.isfile(f"./userbot/modules/{modul}.py"):
        await event.client.send_file(event.chat_id, f"./userbot/modules/{modul}.py", caption=LANG['CYBER_PLUGIN_CAPTION'])
        await event.delete()
    else:
        await event.edit(LANG['NOT_FOUND_PLUGIN'])


@register(cyber=True, pattern="^.ptest")
async def ptest(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        skanet = await yoxla(reply_message)
    else:
        await event.edit(LANG["REPLY_TO_FILE"])
        return

    await event.edit(LANG["DOWNLOADING"])
    if not os.path.exists('./userbot/temp_plugins/'):
        os.makedirs('./userbot/temp_plugins')
    dosya = await event.client.download_media(reply_message, "./userbot/temp_plugins/")
    
    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"{LANG['PLUGIN_BUGGED']} {e}")
        return os.remove("./userbot/temp_plugins/" + dosya)

    return await event.edit(f'☃️ **Modul uğurla yükləndi!**\n\n🎄 __Modulu yoxlaya bilərsiniz.\nBotu yenidən başlatdığınızda plugin işləməyəcəkdir.__')


async def yoxla(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
                return False
            if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data
