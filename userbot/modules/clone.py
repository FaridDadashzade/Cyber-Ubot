# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import html
import os
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import AboutTooLongError
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot.events import register
from telethon.tl import functions
from userbot import TEMP_DOWNLOAD_DIRECTORY, bot, DEFAULT_BIO, DEFAULT_NAME, BRAIN_CHECKER, WHITELIST, SUPPORT
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("admin")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.klon ?(.*)")
@register(outgoing=True, pattern="^.clone ?(.*)")
async def clone(event):
    if event.fwd_from:
        return
    if event.is_reply:
        reply = await event.get_reply_message()
        reply_user = await event.client.get_entity(reply.from_id)
        if reply_user.id in BRAIN_CHECKER or reply_user.id in WHITELIST:
            await event.edit("Bağışlayın, ama bir C Y B Ξ R UserBot adminini klonlamayacağam!")
            return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, TEMP_DOWNLOAD_DIRECTORY)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
      last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"

    #user_bio = replied_user.about
    #if user_bio is not None:
        #user_bio = html.escape(replied_user.about)
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    #await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    n = 1
    pfile = await event.client.upload_file(profile_pic)
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await event.delete()
    await event.client.send_message(event.chat_id,"`C Y B Ξ R Userbot vasitəsilə səni oğurladım..`", reply_to=reply_message)


@register(outgoing=True, pattern="^.revert ?(.*)")
async def revert(event):
    if event.fwd_from:
        return

    if DEFAULT_NAME:
        name = f"{DEFAULT_NAME}"
    else:
        await event.edit("**Xahiş edirəm hər-hansı bir qrupa** `.set var DEFAULT_NAME adınız` **yazıb göndərin.**")
        return

    n = 1
    try:
        await bot(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=n)))
        await bot(functions.account.UpdateProfileRequest(first_name=DEFAULT_NAME))
        await bot(functions.account.UpdateProfileRequest(about=DEFAULT_BIO))
        await event.edit(f"`{DEFAULT_NAME}, hesabınız uğurla köhnə halına qaytarıldı!`")
    except AboutTooLongError:
        srt_bio = "@TheCyberUserBot"
        await bot(functions.account.UpdateProfileRequest(about=srt_bio))
        await event.edit("`Hesabınız uğurla köhnə halına qaytarıldı!\nAmma bio'nuz çox uzun olduğu üçün hazır bio-dan istifadə etdim.`")


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit(LANG['PLEASE_REPLY'])
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra

            
Help = CmdHelp('klon')
Help.add_command('clone', '<bir istifadəçiyə cavab olaraq>', 'Qeyd etdiyiniz istifadəçinin klonu olarsınız.')
Help.add_command('revert', None, 'Hesabınızı əvvəlki halına qaytarar.')
Help.add_info('@TheCyberUserBot')
Help.add()
