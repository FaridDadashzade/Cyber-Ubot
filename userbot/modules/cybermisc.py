# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import requests
import re
import datetime
import logging
import bs4
import os
import asyncio
import time
import html
from telethon import *
from telethon import events
from telethon import utils
from telethon.tl import functions
from datetime import datetime
from userbot.cmdhelp import CmdHelp
from userbot import bot, WHITELIST
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently, ChatBannedRights, ChannelParticipantsKicked
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.errors.rpcerrorlist import YouBlockedUserError
from asyncio import sleep
from userbot.events import register
from userbot import BOTLOG_CHATID, BOTLOG, SUDO_ID

from userbot.language import get_value
LANG = get_value("admin")


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit(f"**Xahiş edirəm bir istifadəçiyə cavab verin\nvə ya istifadəçi adı qeyd edin.**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Xəta baş verdi! \n **XƏTA**\n", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

try:
    from userbot import client2, client3
except BaseException:
    client2 = client3 = None

@register(outgoing=True, pattern="^.banall")
async def banall(event):
    await event.edit("`Qrup boşaldılır...`")
    me = await event.client.get_me()
    all_participants = await event.client.get_participants(event.chat_id)
    for user in all_participants:
        if user.id == me.id:
            pass
        try:
            await event.client(EditBannedRequest(
                event.chat_id, int(user.id), ChatBannedRights(
                    until_date=None,
                    view_messages=True
                )
            ))
        except Exception as e:
            await event.reply(str(e))
        await asyncio.sleep(0.3)


@register(outgoing=True, disable_errors=True, pattern=r"^\.gkick(?: |$)(.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.cgkick$")
async def gspide(rk):
    lazy = rk
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.edit("`İstifadəçi bütün qruplardan atılır..`")
    else:
        rkp = await lazy.edit("`İstifadəçi bütün qruplardan atılır...`")
    me = await rk.client.get_me()
    await rkp.edit(f"**Hazırlanır...**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    else:
        rk.chat.title
    try:
        user, reason = await get_user_from_event(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = 'Gizli'
    except BaseException:
        return await rkp.edit(f"**Xəta!\nNaməlum istifadəçi.**")
    if user:
        if user.id in WHITELIST:
            return await rkp.edit(LANG['BRAIN'])
        try:
            await rk.client(BlockRequest(user))
            await rk.client(UnblockRequest(user))
        except BaseException:
            pass
        testrk = [d.entity.id for d in await rk.client.get_dialogs() if (d.is_group or d.is_channel)]
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, view_messages=False)
                await rk.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await rkp.edit(f"**İstifadəçi qrup/kanallardan atılır.\n{a} qrup/kanaldan atıldı...**")

            except BaseException:
                b += 1
    else:
        await rkp.edit(f"**Bir istifadəçiyə cavab verin.**")

    return await rkp.edit(f"**[{user.first_name}](tg://user?id={user.id}) {a} qrup/kanallardan atıldı.**")

		
@register(outgoing=True, pattern="^.pm ?(.*)")
async def pm(event):
 
    p = event.pattern_match.group(1)
    m = p.split(" ")

    chat_id = m[0]
    try:  
        chat_id = int(chat_id)
    except BaseException:
        
        pass
  
    msg = ""
    mssg = await event.get_reply_message() 
    if event.reply_to_msg_id:
        await event.client.send_message(chat_id, mssg)
        await event.edit("**C Y B Ξ R mesajınızı göndərdi ✔️**")
    for i in m[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await event.client.send_message(chat_id, msg)
        await event.edit("**C Y B Ξ R mesajınızı göndərdi ✔️**")
    except BaseException:
        await event.edit("@TheCyberUserBot mesajınızı göndərə bilmədi :(")
	
	
@register(outgoing=True, pattern=r"^\.tik(?: |$)(.*)")
@register(outgoing=True, pattern=r"^\.tiktok(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit(
            "`Video yükləmək mənə bir link verin!`"
        )
    else:
        await event.edit("```Hazırlanır...```")
    chat = "@SaveOFFbot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit(
                f"**Xəta:** `{chat} blokunu açın və yenidən yoxlayın!`"
            )
            return
        await bot.send_file(event.chat_id, video, caption="Downloaded by [C Y B Ξ R](https://t.me/TheCyberUserBot)")
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, r.id, msg.id, details.id, video.id]
        )
        await event.delete()
	
@register(outgoing=True, pattern=r"^\.insta(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit(
            "`Video yükləmək mənə bir link verin!`"
        )
    else:
        await event.edit("```Hazırlanır...```")
    chat = "@instadowbot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit(
                f"**Xəta:** `{chat} blokunu açın və yenidən yoxlayın!`"
            )
            return
        await bot.send_file(event.chat_id, video, caption="Downloaded by [C Y B Ξ R](https://t.me/TheCyberUserBot)")
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, r.id, msg.id, details.id, video.id]
        )
        await event.delete()
	
@register(outgoing=True, pattern=r"^\.pinterest(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".it" not in d_link:
        await event.edit(
            "`Video yükləmək mənə bir link verin!`"
        )
    else:
        await event.edit("```Hazırlanır...```")
    chat = "@pinterest_downloaderbot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit(
                f"**Xəta:** `{chat} blokunu açın və yenidən yoxlayın!`"
            )
            return
        await bot.send_file(event.chat_id, video, caption="Downloaded by [C Y B Ξ R](https://t.me/TheCyberUserBot)")
        await event.client.delete_messages(
            conv.chat_id, [msg_start.id, r.id, msg.id, details.id, video.id]
        )
        await event.delete()
	      

@register(outgoing=True, groups_only=True, pattern="^.undelete(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=10, edit=False, delete=True
        )
        silinen_msjlar = "Bu qrupdaki silinmiş 10 mesaj:\n\n"
        for i in a:
            silinen_msjlar += "\n💥{}".format(i.old.message) #thx https://github.com/H1M4N5HU0P/MAFIA-USERBOT/blob/97a6874172ee3e2e1a6fe647ea925abd14cba3fb/userbot/plugins/admin.py#L380
        await event.edit(silinen_msjlar)
    else:
        await event.edit("Bunu etmək üçün admin olmalısınız."
        )
        await sleep(3)
        try:
            await event.delete()
        except:
            pass
	

@register(outgoing=True, groups_only=True, disable_errors=True, pattern=r"^\.unbanall(?: |$)(.*)")
async def _(cyber):
    await cyber.edit("`Qadağan olunmuş istifadəçiləri axtarıram...`")
    p = 0
    (await cyber.get_chat()).title
    async for i in cyber.client.iter_participants(
        cyber.chat_id,
	filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await cyber.client.edit_permissions(cyber.chat_id, i, view_messages=True)
            p += 1
        except BaseException:
            pass
    await cyber.edit("`Qadağan olunmuş istifadəçilər siyahıdan silindi...`")
	
	
	
@register(outgoing=True, disable_errors=True, pattern=r"^\.oxu(?: |$)(.*)")
@register(outgoing=True, disable_errors=True, pattern=r"^\.open(?: |$)(.*)")
async def _(event):
    await event.delete()
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    a = await event.reply("**Fayl oxunur...**")
    if len(c) > 4095:
        await a.edit("`Bağışlayın, bir xəta baş verdi.`")
    else:
        await event.client.send_message(event.chat_id, f"```{c}```")
        await a.delete()
    os.remove(b)


@register(outgoing=True, disable_errors=True, pattern=r"^\.repack(?: |$)(.*)")
async def _(event):
    await event.delete()
    a = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    b = open(input_str, "w")
    b.write(str(a.message))
    b.close()
    a = await event.reply(f"`{input_str}` **hazırlanır...**")
    await asyncio.sleep(2)
    await a.edit(f"`{input_str}` **göndərilir...**")
    await asyncio.sleep(2)
    await event.client.send_file(event.chat_id, input_str)
    await a.delete()
    os.remove(input_str)
	
	
@register(outgoing=True, pattern=r"^\.pdf(?: |$)(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await event.edit("**Xahiş edirəm bir mesaja cavab verin!**")
    reply_message = await event.get_reply_message()
    chat = "@office2pdf_bot"
    await event.edit("`Hazırlanır..`")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                wait = await conv.send_message(reply_message)
                convert = await conv.send_message("/ready2conv")
                confirm = await conv.get_response()
                editfilename = await conv.send_message("Yes")
                enterfilename = await conv.get_response()
                filename = await conv.send_message("@thecyberuserbot")
                started = await conv.get_response()
                pdf = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("**Xahiş edirəm @office2pdf_bot blokdan çıxarın və sonra yoxlayın.**")
                return
            await event.client.send_message(event.chat_id, pdf)
            await event.client.delete_messages(
                conv.chat_id,
                [
                    msg_start.id,
                    response.id,
                    wait.id,
                    started.id,
                    filename.id,
                    editfilename.id,
                    enterfilename.id,
                    confirm.id,
                    pdf.id,
                    convert.id,
                ],
            )
            await event.delete()
    except TimeoutError:
        return await event.edit(
            "**Xəta: @office2pdf_bot cavab vermir biraz sonra yoxlayın.**"
        )	
	
@register(outgoing=True, pattern="^.sendbot (.*)")
async def sendbot(cyber):
    if cyber.fwd_from:
        return
    chat = str(cyber.pattern_match.group(1).split(' ', 1)[0])
    link = str(cyber.pattern_match.group(1).split(' ', 1)[1])
    if not link:
        return await cyber.edit("`Bağışlayın, heçnə tapa bilmədim.`")
     
    botid = await cyber.client.get_entity(chat)
    await cyber.edit("```Hazırlanır...```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=botid))
              msg = await bot.send_message(chat, link)
              response = await response
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError: 
              await cyber.reply(f"`Xahiş edirəm` {chat} `-u blokdan çıxarın və yenidən yoxlayın.`")
              return
          except :
              await cyber.edit("`Belə bir bot yoxdur :(`")
              await sleep(2)
              return await cyber.delete()
         
          await cyber.edit(f"`Göndərilən mesaj` : {link}"
                               f"\n`Kimə` : {chat}")
          await bot.send_message(cyber.chat_id, response.message)
          await bot.send_read_acknowledge(cyber.chat_id)
          """ prosesi yerine yetirdikden sonra silmesi ucun """
          await cyber.client.delete_messages(conv.chat_id,
                                                [msg.id, response.id])

		
	
Help = CmdHelp('cybermisc')
Help.add_command('undelete', None, 'Bir qrupda silinmiş 10 mesajı göndərər.')
Help.add_command('unbanall', None, 'Qrupda qadağan edilmiş bütün istifadəçilərin qadağasını silər.')
Help.add_command('sendbot', '<@botun-istifadeci-adi> <mesaj>', 'Yazdığınız əmri qeyd etdiyiniz bota göndərər və botun cavabını atar')
Help.add()


Help = CmdHelp('pm')
Help.add_command('pm', '<@istifadeci-adi> <mesaj>', 'Qeyd etdiyiniz mesajı istədiyiniz şəxsə göndərər.')
Help.add()


Help = CmdHelp('banall')
Help.add_command('banall', None, 'Admin olduğunuz qrupda insanları qrupdan avtomatik ban edər.')
Help.add_info('@TheCyberUserBot məsuliyyət daşımır.')
Help.add()


Help = CmdHelp('social')
Help.add_command('tik', '<link>', 'TikTok-dan video yükləyər.')
Help.add_command('insta', '<link>', 'Instagram-dan video və ya şəkil yükləyər.')
Help.add_command('pinterest', '<link>', 'Pinterest-dən video və ya şəkil yükləyər.')
Help.add_info('@TheCyberUserBot')
Help.add()

Help = CmdHelp('files')
Help.add_command('oxu', '<bir fayla cavab>', 'Faylın məzmununu oxuyun və Telegram mesajı olaraq göndərin.')
Help.add_command('repack', '<bir mətnə cavab> <fayl_adı.py>', 'Cavab verdiyiniz mətni plugin edib atar.')
Help.add_command('pdf', '<bir mediaya və ya mətnə cavab>', 'Cavab verdiyiniz mətni və ya şəkili pdf-yə çevirər.')
Help.add()
