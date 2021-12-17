# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import os
from telethon.tl.functions.contacts import UnblockRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from telethon import events

chat = "@BotFather"

@register(outgoing=True, pattern="^.botfather ?(.*)")
async def _(event):
    if event.pattern_match.group(1):
        text, username= event.pattern_match.group(1).split()
        
    else:
        await event.edit("`Botu yaratmaq üçün <bot_adı><bot_istifadəçi_adı> qeyd edin.`")
        return

    async with event.client.conversation("@BotFather") as conv:
        try:
            await conv.send_message("/newbot")
            audio = await conv.get_response()
            await conv.send_message(text)
            audio = await conv.get_response()
            await conv.send_message(username)
            audio = await conv.get_response()
            await event.client.forward_messages("me", audio)
            await event.edit('Məlumatlar kayıtlı mesajlara qeyd edildi.')
        except YouBlockedUserError:
            await event.client(UnblockRequest("93372553"))
            await conv.send_message("/newbot")
            audio = await conv.get_response()
            await conv.send_message(text)
            audio = await conv.get_response()
            await conv.send_message(username)
            audio = await conv.get_response()
            await event.client.forward_messages("me", audio)
            await event.edit('Məlumatlar kayıtlı mesajlara qeyd edildi.')
            await event.delete()


Help = CmdHelp('botfather')
Help.add_command("botfather", "<bot_adı><bot_istifadəçi_adı>", "Bot yaratmağınıza kömək edər.").add()
