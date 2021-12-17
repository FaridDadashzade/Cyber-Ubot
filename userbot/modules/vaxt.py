# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from asyncio import sleep
from telethon.errors import rpcbaseerrors
from userbot.cmdhelp import CmdHelp
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register as cyber

@cyber(outgoing=True, pattern=r"^\.sd")
async def selfdestruct(destroy):
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    cyber = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await cyber.delete()

    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID,
                                          "`Özünü məhv edən mesaj göndərildi və silindi...`")

CmdHelp('mesaj').add_command(
    'sd', '<vaxt + mesaj>', 'Yazdığınız mesajı qeyd etdiyiniz vaxt ərzində silər.'
).add()
