from telethon import events, Button
from ALBY import ALBY
from ALBY.status import *
from Config import Config
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

@ALBY.on(events.callbackquery.CallbackQuery(data="admin"))
async def _(event):

    await event.edit(ADMIN_TEXT, buttons=[[Button.inline("« Kembali", data="help")]])

@ALBY.on(events.callbackquery.CallbackQuery(data="play"))
async def _(event):

    await event.edit(PLAY_TEXT, buttons=[[Button.inline("« Kembali", data="help")]])

@ALBY.on(events.NewMessage(pattern="^[!?/]promote ?(.*)"))
@is_admin
async def promote(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
       await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
       return

    if not perm.add_admins:
        await event.reply("Perintah ini hanya bisa digunakan admin, dan ❌ Anda Bukan Admin Group!❌")
        return
    input_str = event.pattern_match.group(1)
    user = await event.get_reply_message()
    if not input_str and not user:
        await event.reply("Balas pesan pengguna atau berikan username pengguna untuk diangkat menjadi admin!")
        return
    sed = await ALBY(GetFullUserRequest(id=user.sender_id or input_str))
    await Stark(EditAdminRequest(event.chat_id, user.sender_id or input_str, ChatAdminRights(
                    add_admins=False,
                    invite_users=True,
                    change_info=False,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True), rank="Admin"))

    if not input_str:
        await event.reply(f"Berhasil diangkat menjadi Admin [{sed.user.first_name}](tg://user?id={user.sender_id}) in {event.chat.title}!")
        return

    await event.reply(f"Berhasil diangkat menjadi Admin {input_str} in {event.chat.title}")
 
@ALBY.on(events.NewMessage(pattern="^[!?/]demote ?(.*)"))
@is_admin
async def promote(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
       await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
       return
    if not perm.add_admins:
        await event.reply("Perintah ini hanya bisa digunakan admin, dan ❌ Anda Bukan Admin Group!❌")
        return
    input_str = event.pattern_match.group(1)
    user = await event.get_reply_message()
    if not input_str and not user:
        await event.reply("Balas pesan pengguna atau berikan username pengguna untuk menurunkan hak admin!")
        return
    sed = await ALBY(GetFullUserRequest(id=user.sender_id or input_str))
    await Stark(EditAdminRequest(event.chat_id, user.sender_id or input_str, ChatAdminRights(
                    add_admins=False,
                    invite_users=None,
                    change_info=None,
                    ban_users=None,
                    delete_messages=None,
                    pin_messages=None), rank="Not Admin"))

    if not input_str:
        await event.reply(f"Berhasil Diturunkan admin [{sed.user.first_name}](tg://user?id={user.sender_id}) in {event.chat.title}!")
        return

    await event.reply(f"Berhasil Diturunkan admin {input_str} in {event.chat.title}")
 

@ALBY.on(events.NewMessage(pattern="^[!?/]invitelink"))
async def invitelink(event):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
       await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
       return
    link = await ALBY(ExportChatInviteRequest(event.chat_id))
    await event.reply(f"Link grup dari {event.chat.title} is [here]({link.link})", link_preview=False)

ADMIN_TEXT = """
**✘ Modul yang dapat digunakan oleh admin grup!**

‣ `?promote` - Untuk Mengangkat pengguna menjadi admin dalam grup.
‣ `?demote` - Untuk Menurunkan pengguna dari hak admin dalam grup.
‣ `?invitelink` - Untuk mendapatkan tautan undangan grup.
‣ `?end` - Untuk Mengakhiri musik.
‣ `?skip` - Untuk Melewati Trek Terjadi.
‣ `?pause` - Untuk Menjeda musik.
‣ `?resume` - Untuk melanjutkan musik.
‣ `?leavevc` - memaksa Asisten untuk meninggalkan Vc Chat (Terkadang Bergabung).
‣ `?playlist` - untuk memeriksa daftar putar.
"""

PLAY_TEXT = """
**✘ Modul yang dapat digunakan oleh pengguna obrolan!**

‣ `?play` - Untuk Memutar Musik atau Balas ke file audio.
‣ `?vplay` - Untuk Memutar Video (HEROKU_MODE > Tidak mendukung).
"""
