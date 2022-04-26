# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import asyncio
import os
from userbot import bot
from userbot.events import register

@register(cyber=True, pattern="^.meadmin ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    melumatlar_msg = await event.edit("`Məlumatlar əldə edilir..`")
    admin_siyahisi = []
    dialogue = await bot.get_dialogs()
    for dialog in dialogue:
        if dialog.is_group or dialog.is_channel:
            ids = await bot.get_entity(dialog)
            try:
                if ids.admin_rights or ids.creator:
                    info = f"{ids.id}:  {ids.title}"
                    admin_siyahisi.append(info)
            except BaseException:
                pass
            except Exception:
                continue

    if len(admin_siyahisi) > 0:
        with open('admin_siyahı.txt', 'w') as fayl:
            for qruplar_ve_kanallar in admin_siyahisi:
                fayl.write(qruplar_ve_kanallar + '\n')
        await asyncio.sleep(1)
        caption = f'Admin olduğum qrup və kanalların siyahısı.\n\nÜmumi: {len(admin_siyahisi)}'
        try:
            await bot.send_file("me", "admin_siyahı.txt", caption=caption)
            await melumatlar_msg.edit("`Məlumatlar kayıtlı mesajlarınıza göndərildi :)`")
            os.remove("admin_siyahı.txt")
        except Exception:
            await melumatlar_msg.edit("`Bağışlayın, mən heçbir qrupda admin deyiləm :(`")

Help = CmdHelp('meadmin')
Help.add_command('meadmin',  None, 'Admin olduğunuz kanal və qrupların adlarını və ID-lərini bir fayl şəklində göndərər.').add()


