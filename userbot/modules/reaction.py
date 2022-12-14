# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

# CODER tg/@FVREED github/@FaridDadashzade#

from email import message
from userbot.events import register 
from userbot import bot
import emoji
from telethon.tl.functions.messages import SendReactionRequest
from userbot.cmdhelp import CmdHelp

EMOJILER = ["๐", "๐", "โค๏ธ", "๐ฅ", "๐", "๐", "๐คฌ", "๐คฉ", "๐คฎ", "๐ฉ", "๐"]

@register(cyber=True, pattern="^.react (.*)")
async def react(event):
    reply = await event.get_reply_message()
    reaksiya = event.pattern_match.group(1)
    if reaksiya not in EMOJILER:
        await event.edit("**Yanlฤฑล bir emoji qeyd etdiniz!**\n\n**Mรถvcud emojilษr:** `๐, ๐, โค๏ธ, ๐ฅ, ๐, ๐, ๐คฌ, ๐คฉ, ๐คฎ, ๐ฉ, ๐`")
        return
    if not reply:
        await event.edit("**Reaksiya vermษk รผรงรผn bir mesaja cavab verin!**\n\n**ฤฐstifadษsi:** `.react` `๐, ๐, โค๏ธ, ๐ฅ, ๐, ๐, ๐คฌ, ๐คฉ, ๐คฎ, ๐ฉ, ๐`")
        return
    elif "๐" == reaksiya:
        reaksiya = emoji.emojize(':thumbs_up:')
    elif "๐" == reaksiya:
        reaksiya = emoji.emojize(':thumbs_down:')
    elif "โค๏ธ" == reaksiya:
        reaksiya = emoji.emojize(':red_heart:')
    elif "๐ฅ" == reaksiya:
        reaksiya = emoji.emojize(':fire:')
    elif "๐" == reaksiya:
        reaksiya = emoji.emojize(':clapping_hands:')
    elif "๐" == reaksiya:
        reaksiya = emoji.emojize(':beaming_face_with_smiling_eyes:')
    elif "๐คฌ" == reaksiya:
        reaksiya = emoji.emojize(':face_with_symbols_on_mouth:')
    elif "๐คฉ" == reaksiya:
        reaksiya = emoji.emojize(':star-struck:')
    elif "๐คฎ" == reaksiya:
        reaksiya = emoji.emojize(':face_vomiting:')
    elif "๐ฉ" == reaksiya:
        reaksiya = emoji.emojize(':pile_of_poo:')
    elif "๐" == reaksiya:
        reaksiya = emoji.emojize(':folded_hands:')
    elif "๐ฅฑ" == reaksiya:
        reaksiya = emoji.emojize(':yawning_face:')
    elif "๐ฅด" == reaksiya:
        reaksiya = emoji.emojize(':woozy_face:')
    try: 
        message_id = reply.id
        await event.delete()   
        await bot(SendReactionRequest(peer=event.chat_id, msg_id=message_id, reaction=reaksiya))
    except Exception as e:
        await event.edit(e)

Help = CmdHelp('reaction')
Help.add_command('react', '<emoji>', 'Cavab verdiyiniz mesaja reaksiya bildirษr', 'react ๐')
Help.add_info('Mรถvcud emojilษr: ๐, ๐, โค๏ธ, ๐ฅ, ๐, ๐, ๐คฌ, ๐คฉ, ๐คฎ, ๐ฉ, ๐')
Help.add()