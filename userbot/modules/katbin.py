# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

""" Katbin """

from requests import post
from telethon.tl.types import MessageMediaWebPage

from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot import BOTLOG, BOTLOG_CHATID


# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("dogbin")

# ████████████████████████████████ #


@register(outgoing=True, pattern=r"^\.paste(?:\s|$)([\s\S]*)")
@register(outgoing=True, pattern=r"^\.katbin(?:\s|$)([\s\S]*)")
async def paste(event):
    await event.edit(LANG['PASTING'])

    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.media and not isinstance(reply.media, MessageMediaWebPage):
            return await event.edit(LANG['ELON_SAYS'])
        message = reply.message

    elif event.pattern_match.group(1).strip():
        message = event.pattern_match.group(1).strip()

    else:
        return await event.edit("**İstifadəsi** `.cyber katbin`**.**")

    response = post("https://api.katb.in/api/paste", json={"content": message}).json()

    if response["msg"] == "Successfully created paste":
        await event.edit(f"{LANG['URL']} [Katb.in](https://katb.in/{response['paste_id']})\n")
    else:
        await event.edit("**Katb.in saytı ilə bağlı bir xəta baş verdi.**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Qeyd etdiyiniz mətn uğurla Katb.in saytına yapışdırıldı.",
        )

CmdHelp('katbin').add_command(
    'paste', '<söz/yanıtlama>', 'Katbin işlədərək yapışdırılmış və ya qısadılmış url yaratma (https://katb.in/)'
).add()
