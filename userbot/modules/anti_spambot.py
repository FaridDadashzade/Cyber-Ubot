# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

from asyncio import sleep
from requests import get
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, ANTI_SPAMBOT, ANTI_SPAMBOT_SHOUT, bot


@bot.on(ChatAction)
async def anti_spambot(welcm):
    try:
        if not ANTI_SPAMBOT:
            return
        if welcm.user_joined or welcm.user_added:
            adder = None
            ignore = False
            users = None

            if welcm.user_added:
                ignore = False
                try:
                    adder = welcm.action_message.from_id
                except AttributeError:
                    return

            async for admin in bot.iter_participants(
                    welcm.chat_id, filter=ChannelParticipantsAdmins):
                if admin.id == adder:
                    ignore = True
                    break

            if ignore:
                return

            elif welcm.user_joined:
                users_list = hasattr(welcm.action_message.action, "users")
                if users_list:
                    users = welcm.action_message.action.users
                else:
                    users = [welcm.action_message.from_id]

            await sleep(5)
            spambot = False

            if not users:
                return

            for user_id in users:
                async for message in bot.iter_messages(welcm.chat_id,
                                                       from_user=user_id):

                    correct_type = isinstance(message, Message)
                    if not message or not correct_type:
                        break

                    join_time = welcm.action_message.date
                    message_date = message.date

                    if message_date < join_time:
                        # Eğer mesaj kullanıcı katılma tarihinden daha önce ise yoksayılır.
                        continue

                    check_user = await welcm.client.get_entity(user_id)

                    # Hata ayıklama. İlerideki durumlar için bırakıldı. ###
                    print(
                        f"Qatılan istifadəçi: {check_user.first_name} [ID: {check_user.id}]"
                    )
                    print(f"Qrup: {welcm.chat.title}")
                    print(f"Zaman: {join_time}")
                    print(
                        f"Göndərdiyi mesaj: {message.text}\n\n[Zaman: {message_date}]"
                    )
                    ##############################################

                    try:
                        cas_url = f"https://combot.org/api/cas/check?user_id={check_user.id}"
                        r = get(cas_url, timeout=3)
                        data = r.json()
                    except BaseException:
                        print(
                            "CAS kontrolu uğursuzdur, köhnə anti_spambot kontroluna qayıdılır."
                        )
                        data = None
                        pass

                    if data and data['ok']:
                        reason = f"[Combot Anti Spam tərəfindən banlandı.](https://combot.org/cas/query?u={check_user.id})"
                        spambot = True
                    elif "t.cn/" in message.text:
                        reason = "`t.cn` URL'leri aşkarlandı."
                        spambot = True
                    elif "t.me/joinchat" in message.text:
                        reason = "Qrup və ya kanal reklamı mesajı."
                        spambot = True
                    elif message.fwd_from:
                        reason = "Yönləndirilən mesaj"
                        spambot = True
                    elif "?start=" in message.text:
                        reason = "Telegram botu `start` linki"
                        spambot = True
                    elif "bit.ly/" in message.text:
                        reason = "`bit.ly` URL-i aşkar edildi."
                        spambot = True
                    else:
                        if check_user.first_name in ("Bitmex", "Promotion",
                                                     "Information", "Dex",
                                                     "Announcements", "Info",
                                                     "Broadcast", "Broadcasts"
                                                     "Məlumatlandırma", "Məlumatlandırmalar"):
                            if check_user.last_name == "Bot":
                                reason = "Bilinən SpamBot"
                                spambot = True

                    if spambot:
                        print(f"Spam mesajı: {message.text}")
                        await message.delete()
                        break

                    continue 

            if spambot:
                chat = await welcm.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    if ANTI_SPAMBOT_SHOUT:
                        await welcm.reply(
                            "@admins\n"
                            "`ANTI SPAMBOT AŞKARLANDI!\n"
                            "BU İSTİFADƏÇİ MƏNİM SPAMBOT ALQORİTMAM İLƏ UYĞUNLAŞIR!`"
                            f"SƏBƏB: {reason}")
                        kicked = False
                        reported = True
                else:
                    try:

                        await welcm.reply(
                            "`Spambot aşkarlandı!!`\n"
                            f"`SƏBƏB:` {reason}\n"
                            "Qrupdan atılır, bu ID sonraki proseslər üçün qeyd edilir.\n"
                            f"`İSTİFADƏÇİ:` [{check_user.first_name}](tg://user?id={check_user.id})"
                        )

                        await welcm.client.kick_participant(
                            welcm.chat_id, check_user.id)
                        kicked = True
                        reported = False

                    except BaseException:
                        if ANTI_SPAMBOT_SHOUT:
                            await welcm.reply(
                                "@admins\n"
                                "`ANTİ SPAMBOT AŞKAR EDİLDİ!\n"
                                "BU İSTİFADƏÇİ MƏNİM SPAMBOT ALQORİTMAM İLƏ UYĞUNDUR!`"
                                f"SƏBƏB: {reason}")
                            kicked = False
                            reported = True

                if BOTLOG:
                    if kicked or reported:
                        await welcm.client.send_message(
                            BOTLOG_CHATID, "#ANTI_SPAMBOT BİLDİRİŞ\n"
                            f"İstifadəçi: [{check_user.first_name}](tg://user?id={check_user.id})\n"
                            f"İstifadəçi IDsi: `{check_user.id}`\n"
                            f"Qrup: {welcm.chat.title}\n"
                            f"Qrup IDsi: `{welcm.chat_id}`\n"
                            f"Səbəb: {reason}\n"
                            f"Mesaj:\n\n{message.text}")
    except ValueError:
        pass


CMD_HELP.update({
    'anti_spambot':
    "İstifadəsi: Bu modul config.env faylında ya da env dəyəri ilə aktiv edilibsə,\
        \nəgər spam edənlər UserBot'un anti-spam alqoritması ilə uyğunlaşırsa, \
        \nbu modul qrupdaki spammerləri qrupdan atar. (ya da adminlərə bildirər.)"
})
