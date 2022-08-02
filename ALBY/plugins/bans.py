from ALBY import ALBY
from ALBY.status import *
from Config import Config
from telethon import events, Button
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

BANS_TEXT = """
**✘ Beberapa orang perlu diban secara publik karena spammer dan gangguan.**

‣ `?kickme` - Untuk diri sendiri Menendang(kick) Anda dari obrolan chat.
‣ `?kick` - Untuk menendang(kick) seseorang dari obrolan chat.
‣ `?unban` - Untuk membatalkan pemblokiran(ban) anggota dari obrolan.
‣ `?ban` - Untuk Memblokir(ban) Seseorang dari obrolan.
‣ `?dban` - Untuk menghapus pesan yang dibalas (reply) dan memblokir(ban) pengguna.
‣ `?sban` - Untuk menghapus pesan yang dibalas (reply) dan menendang(kick) pengguna.
‣ `?skick` - Untuk Menghapus pesan Anda dan menendang(kick) pengguna.
‣ `?dkick` - Untuk menghapus pesan Anda dan menendang(kick) pengguna yang dibalas (reply).
"""

@ALBY.on(events.NewMessage(pattern="^[!?/]kick ?(.*)"))
@is_admin
async def kick(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return

    if event.is_private:
        await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
        return
    if not perm.ban_users:
         await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
         return
    input_str = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if not input_str and not msg:
        await event.reply("Balas (reply) ke pengguna atau berikan nama pengguna untuk menendang (kick) nya")
        return

    replied_user = msg.sender_id
    us = msg.sender.username
    info = await Zaid.get_entity(us)
    await Zaid.kick_participant(event.chat_id, input_str or replied_user)
    await event.reply(f"Succesfully Kicked [{info.first_name}](tg://user?id={replied_user}) from {event.chat.title}")

@ALBY.on(events.NewMessage(pattern="^[!?/]kickme"))
async def kickme(event):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
        await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
        return

    check = await Zaid.get_permissions(event.chat_id, event.sender_id)
    if check.is_admin:
        await event.reply("Maaf saya tidak bisa menendang (kick) admin!")
        return

    await event.reply("Oke, sesuai keinginan Anda")
    await Zaid.kick_participant(event.chat_id, event.sender_id)

@ALBY.on(events.NewMessage(pattern="^[!?/]ban ?(.*)"))
@is_admin
async def ban(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
        await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
        return
    if not perm.ban_users:
        await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
        return
    input_str = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if not input_str and not msg:
        await event.reply("Balas (reply) ke pengguna atau berikan nama pengguna untuk memblokir (ban) pengguna")
        return
    replied_user = msg.sender_id
    us = msg.sender.username
    info = await Zaid.get_entity(us)
    await Zaid(EditBannedRequest(event.chat_id, replied_user, ChatBannedRights(until_date=None, view_messages=True)))
    await event.reply(f"Succesfully Banned [{info.first_name}](tg://user?id={replied_user}) in {event.chat.title}")

@ALBY.on(events.NewMessage(pattern="^[!?/]unban ?(.*)"))
@is_admin
async def unban(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
        await event.reply("Perintah ini dibuat untuk digunakan dalam grup, bukan di PM!")
        return
    if not perm.ban_users:
        await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
        return
    input_str = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if not input_str and not msg:
        await event.reply("Balas (reply) ke pengguna atau berikan nama pengguna untuk membatalkan pemblokiran (unban) nya")
        return
    replied_user = msg.sender_id
    us = msg.sender.username
    info = await Zaid.get_entity(us)
    await Zaid(EditBannedRequest(event.chat_id, replied_user, ChatBannedRights(until_date=None, view_messages=False)))
    await event.reply(f"Succesfully Unbanned [{info.first_name}](tg://user?id={replied_user}) in {event.chat.title}")

@ALBY.on(events.NewMessage(pattern="^[!?/]skick"))
@is_admin
async def skick(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.ban_users:
         await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
         return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Balas (reply) seseorang untuk menghapus pesan dan menendang(kick) pengguna")
        return

    us = reply_msg.sender.username
    info = await Zaid.get_entity(us)   
    x = (await event.get_reply_message()).sender_id
    zx = (await event.get_reply_message())
    await event.delete()
    await Zaid.kick_participant(event.chat_id, x)
    await event.reply(f"Succesfully Kicked [{info.first_name}](tg://user?id={replied_user}) from {event.chat.title}")

@ALBY.on(events.NewMessage(pattern="^[!?/]dkick"))
@is_admin
async def dkick(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.ban_users:
         await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
         return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Balas (reply) seseorang untuk menghapus pesan dan menendang(kick) pengguna!")
        return
    us = reply_msg.sender.username
    info = await Zaid.get_entity(us) 
    x = await event.get_reply_message()
    await x.delete()
    await Zaid.kick_participant(event.chat_id, x.sender_id)
    await event.reply(f"Succesfully Kicked [{info.first_name}](tg://user?id={replied_user}) from {event.chat.title}")

@ALBY.on(events.NewMessage(pattern="^[!?/]dban"))
@is_admin
async def dban(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.ban_users:
         await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
         return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Balas (reply) seseorang untuk menghapus pesan dan memblokir(ban) pengguna!")
        return
    us = reply_msg.sender.username
    info = await Zaid.get_entity(us) 
    x = (await event.get_reply_message()).sender_id
    zx = (await event.get_reply_message())
    await zx.delete()
    await Zaid(EditBannedRequest(event.chat_id, x, ChatBannedRights(until_date=None, view_messages=True)))
    await event.reply("Successfully Banned!")
    await event.reply(f"Succesfully Banned [{info.first_name}](tg://user?id={replied_user}) from {event.chat.title}")

@ALBY.on(events.NewMessage(pattern="^[!?/]sban"))
@is_admin
async def sban(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.ban_users:
         await event.reply("Perintah ini hanya bisa digunakan admin yang memiliki hak ban!❌")
         return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("Balas (reply) seseorang untuk menghapus pesan dan memblokir(ban) pengguna!")
        return
    us = reply_msg.sender.username
    info = await Zaid.get_entity(us) 
    x = (await event.get_reply_message()).sender_id
    zx = (await event.get_reply_message())
    await event.delete()
    await Zaid(EditBannedRequest(event.chat_id, x, ChatBannedRights(until_date=None, view_messages=True)))
    await event.reply(f"Succesfully Banned [{info.first_name}](tg://user?id={replied_user}) from {event.chat.title}")

@ALBY.on(events.callbackquery.CallbackQuery(data="bans"))
async def banhelp(event):
    await event.edit(BANS_TEXT, buttons=[[Button.inline("« Kembali", data="help")]])
