# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from userbot.events import register
from userbot import bot, get_call
from userbot.cmdhelp import CmdHelp

def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]

        
@register(cyber=True, disable_errors=True, pattern="^.vcbaslat$")
async def start_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await c.edit("`Bunu etmək üçün admin olmalıyam!`")
        return
    try:
        await c.client(startvc(c.chat_id))
        await c.edit("`Səsli söhbət başladı!`")
    except Exception as ex:
        await c.edit(f"Bir xəta baş verdi\nXəta: `{ex}`")

        
        
@register(cyber=True, disable_errors=True, pattern="^.vctitle$")
async def change_vc_title(e):
    title = e.pattern_match.group(1).lower()
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not title:
        return await e.edit("**Zəhmət olmasa qrup səsli söhbətinin adını daxil edin.**")
    if not admin and not creator:
        await e.edit(f"`Bunu etmək üçün admin olmalıyam!`")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await e.edit(f"**Səsli söhbət başlığı** `{title}` **olaraq ayarlandı.**")
    except Exception as ex:
        await e.edit(f"**Bir xəta baş verdi\nXəta:** `{ex}`")    
        

@register(cyber=True, disable_errors=True, pattern="^.vcbagla$")
async def stop_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await c.edit("`Bunu etmək üçün admin olmalıyam!`")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await c.edit("`Səsli söhbət uğurla sonlandırıldı!`")
    except Exception as ex:
        await c.edit(f"Bir xəta baş verdi\nXəta: `{ex}`")



@register(cyber=True, disable_errors=True, pattern="^.tagvc")
async def _(c):
    await c.edit("`İstifadəçilər səsli söhbətə çağrılır...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    cyber = list(user_list(users, 6))
    for p in cyber:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await c.edit(f"`{z}` **istifadəçi çağırıldı...**")


Help = CmdHelp('voicechat')
Help.add_command('vcbaslat', None, 'Bir qrupda səsli söhbət başladar.')
Help.add_command('vcbagla', None, 'Səsli söhbəti sonlandırar.')
Help.add_command('vctitle', None, 'Səsli söhbətin başlığını dəyişdirmək üçün.')
Help.add_command('tagvc', None, 'Qrupdaki istifadəçiləri səsli söhbətə dəvət edər.')
Help.add_info('@TheCyberUserBot')
Help.add()    
