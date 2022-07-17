# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import io
import math
import urllib.request
from PIL import Image
import os 
import cloudscraper
from bs4 import BeautifulSoup as bs
import time
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto, InputPeerNotifySettings
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot, PAKET_ISMI
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import events
import random
from userbot.cmdhelp import CmdHelp

PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."
PACK_DOESNT_EXIST = "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("stickers")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.ogurla($| )?((?![0-9]).+?)? ?([0-9]*)?")
@register(outgoing=True, pattern="^.dızla($| )?((?![0-9]).+?)? ?([0-9]*)?")
@register(outgoing=True, pattern="^.kang($| )?((?![0-9]).+?)? ?([0-9]*)?")
async def kang(event):
    await event.edit(f"`{PLUGIN_MESAJLAR['dızcı']}`")
    user = await bot.get_me()
    pack_username = ''
    if not user.username:
        try:
            user.first_name.decode('ascii')
            pack_username = user.first_name
        except (UnicodeDecodeError, AttributeError):
            pack_username = user.id
    else:
        pack_username = user.id


    textx = await event.get_reply_message()
    if not textx:
        await event.edit(LANG['GIVE_STICKER'])
        return
    emoji = event.pattern_match.group(2)
    number = int(event.pattern_match.group(3) or 1)
    new_pack = False

    if textx.photo or textx.sticker: message = textx
    elif event.photo or event.sticker: message = event
    else:
        await event.edit(LANG['GIVE_STICKER'])
        return

    sticker = io.BytesIO()
    await bot.download_media(message, sticker)
    sticker.seek(0)

    if not sticker:
        await event.edit(LANG['FAIL_DOWNLOAD'])
        return

    is_anim = message.file.mime_type == "application/x-tgsticker"
    if not is_anim:
        img = await resize_photo(sticker)
        sticker.name = "cyber.png"
        sticker.seek(0)
        img.save(sticker, "PNG")


    if not emoji:
        if message.file.emoji: 
            emoji = message.file.emoji
        else: 
            random_emoji = "🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 ☺️ 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍧 🍨".split(" ")
            emoji = random.choice(random_emoji)
    
    if user.username:
        hashtag = "@"
    else:
        hashtag = ""

    packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
    packtitle = (f"{hashtag}{user.username or user.first_name} {PAKET_ISMI} "
                f"{number}{' animasyonlu' if is_anim else ''}")
    response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
    htmlstr = response.read().decode("utf8").split('\n')
    new_pack = PACK_DOESNT_EXIST in htmlstr

    if new_pack:
        await event.edit(LANG['NEW_PACK'])
        await newpack(is_anim, sticker, emoji, packtitle, packname, message)
    else:
        async with bot.conversation("Stickers") as conv:
            await conv.send_message('/cancel')
            await conv.get_response()

            await conv.send_message('/addsticker')
            await conv.get_response()

            await conv.send_message(packname)
            x = await conv.get_response()

            while x.text == PACK_FULL:
                number += 1
                packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
                packtitle = (f"@{user.username or user.first_name} {PAKET_ISMI} "
                            f"{number}{' animated' if is_anim else ''}")

                await event.edit(
                    LANG['TOO_STICKERS'].format(number)
                )

                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text == "Invalid pack selected.":
                    await newpack(is_anim, sticker, emoji, packtitle, packname)

                    await bot.send_read_acknowledge("stickers")
                    muted = await bot(UpdateNotifySettingsRequest(
                        peer=429000,
                        settings=InputPeerNotifySettings(mute_until=None))
                    )

                    await event.edit(
                        f"`Stiker {number}{'(animasyonlu)' if is_anim else ''} saylı paketə əlavə edildi, "
                        f"{emoji} emojisi ilə birlikdə! "
                        f"Paket `[burada](t.me/addstickers/{packname})`tapıla bilər`",
                        parse_mode='md')
                    return

            if is_anim:
                upload = await message.client.upload_file(sticker, file_name="AnimatedSticker.tgs")
                await conv.send_file(upload, force_document=True)
            else:
                sticker.seek(0)
                await conv.send_file(sticker, force_document=True)
            kontrol = await conv.get_response()
        
            if "Sorry, the image dimensions are invalid." in kontrol.text:
                await event.edit("`Sticker's kabul etmedi. İkinci yöntem deneniyor...`")
                try:
                    await bot.send_file("@ezstickerbot", message, force_document=True)
                except YouBlockedUserError:
                    return await event.edit("`Xahiş` @EzStickerBot `bloku açın və təkrar yoxlayın!`")

                try:
                    response = await conv.wait_event(events.NewMessage(incoming=True,from_users=350549033))
                    if "Please temporarily use" in response.text:
                        await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                        response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                
                    await bot.send_read_acknowledge(350549033)
                    await event.client.forward_messages("stickers", response.message, 350549033)
                except:
                    await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                    response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                    await bot.send_read_acknowledge(891811251)
                    await event.client.forward_messages("stickers", response.message, 891811251)

            await conv.send_message(emoji)
            await conv.get_response()

            await conv.send_message('/done')
            await conv.get_response()

    await bot.send_read_acknowledge(429000)
    muted = await bot(UpdateNotifySettingsRequest(
        peer=429000,
        settings=InputPeerNotifySettings(mute_until=None))
    )

    await event.edit(
        f"`Stiker {number}{'(animasyonlu)' if is_anim else ''} saylı paketə əlavə edildi, "
        f"{emoji} emojisi ilə birlikdə! "
        f"Paket `[burada](t.me/addstickers/{packname})` tapıla bilər.`",
        parse_mode='md')


async def newpack(is_anim, sticker, emoji, packtitle, packname, message):
    async with bot.conversation("stickers") as conv:
        await conv.send_message('/cancel')
        await conv.get_response()

        if is_anim:
            await conv.send_message('/newanimated')
        else:
            await conv.send_message('/newpack')
        await conv.get_response()

        await conv.send_message(packtitle)
        await conv.get_response()

        if is_anim:
            upload = await bot.upload_file(sticker, file_name="AnimatedSticker.tgs")
            await conv.send_file(upload, force_document=True)
        else:
            sticker.seek(0)
            await conv.send_file(sticker, force_document=True)
        kontrol = await conv.get_response()
        if kontrol.message.startswith("Sorry"):
            await bot.send_file("@ezstickerbot", message, force_document=True)
            try:
                response = await conv.wait_event(events.NewMessage(incoming=True,from_users=350549033))
                if "Please temporarily use" in response.text:
                    await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                    response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                
                    await bot.send_read_acknowledge(350549033)
                    await bot.forward_messages("stickers", response.message, 350549033)
            except:
                await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                await bot.send_read_acknowledge(891811251)
                await bot.forward_messages("stickers", response.message, 891811251)
        await conv.send_message(emoji)
        await conv.get_response()
        await conv.send_message("/publish")
        if is_anim:
            await conv.get_response()
            await conv.send_message(f"<{packtitle}>")
        await conv.get_response()
        await conv.send_message("/skip")
        await conv.get_response()
        await conv.send_message(packname)
        await conv.get_response()

async def resize_photo(photo):
    image = Image.open(photo)
    scale = 512 / max(image.width, image.height)
    new_size = (int(image.width*scale), int(image.height*scale))
    image = image.resize(new_size, Image.ANTIALIAS)
    return image


combot_stickers_url = "https://combot.org/telegram/stickers?q="

@register(cyber=True, pattern=r".cstick ?(.*)")
async def cstick(event):
    stiker_paketi_adi = event.pattern_match.group(1)
    if not stiker_paketi_adi:
        await event.edit("`Xahiş edirəm bir stiker paketi adı daxil edin!`\n**İstifadəsi:** `.cstick salam`")
    scraper = cloudscraper.create_scraper()
    text = scraper.get(combot_stickers_url + stiker_paketi_adi).text
    soup = bs(text, 'lxml') 
    neticeler = soup.find_all("a", {"class": "sticker-pack__btn"})
    paket_adi = soup.find_all("div", "sticker-pack__title")

    netice = f"`{stiker_paketi_adi}` **üçün axtarış:**\n"

    if not neticeler:
        return await event.edit("`Təəssüfki belə bir stiker tapılmadı.`")

    for nəticə, ad in zip(neticeler, paket_adi):
        link = nəticə["href"]
        netice += f"\n• [{ad.get_text()}]({link})"
        await event.edit("{}\n\nPowered by @TheCyberUserBot".format(netice))
        time.sleep(0.7)


CmdHelp('stickers').add_command(
    'ogurla', None, 'Bu əmr vasitəsilə bir stikerə və ya şəkilə yanıt verib onu öz paketinizə əlavə edə bilərsiniz.'
).add_command(
    'ogurla', '<emoji(lər)>', 'Oğurla kimi işləyir amma istədiyiniz emojini stikerin emojisi olaraq ayarlayar.'
).add_command(
    'ogurla', '<nömrə>', 'Stikeri ya da şəkili qeyd edilən paketə əlavə edər amma emoji olaraq bu istifadə edilir: ✨ '
).add_command(
    'ogurla', '<emoji(lər)> <nömrə>', 'Stikeri ya da şəkili qeyd edilən paketə əlavə edər və qeyd etdiyiniz emoji stikerin emojisi olaraq istifadə edilir.'
).add()

Help = CmdHelp('cstick')
Help.add_command('cstick', '<stiker paketi adı>', 'Combot saytından yazdığınız sözə uyğun stikerləri gətirər.')
Help.add()