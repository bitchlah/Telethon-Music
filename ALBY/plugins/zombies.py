from telethon import events, Button
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChatBannedRights
from ALBY import ALBY
from ALBY.status import *
from Config import Config

CLEANER_HELP = """
**✘ Ini adalah Modul Untuk Menghapus Akun terhapus Dari Grup Anda!**

‣ `?zombies` - Untuk menemukan akun terhapus di obrolan Anda.
‣ `?zombies clean` - Untuk menghapus akun terhapus dari obrolan Anda.
"""


BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


@ALBY.on(events.NewMessage(pattern="^[!?/]zombies ?(.*)"))
@is_admin
async def clean(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.ban_users:
      await event.reply("Anda tidak memiliki hak")
      return
    input_str = event.pattern_match.group(1)
    stats = "Group sudah bersih."
    deleted = 0

    if "clean" not in input_str:
      zombies = await event.respond("Mencari Zombie/Akun Terhapus...")
      async for user in event.client.iter_participants(event.chat_id):

            if user.deleted:
                deleted += 1
      if deleted > 0:
            stats = f"Ditemukan **{deleted}** Zombie/Akun Terhapus Di Grup Ini.\
            \nBersihkan Akun Terhapus Dengan Menggunakan - `/zombies clean`"
      await zombies.edit(stats)
      return

    cleaning_zombies = await event.respond("Membersihkan Zombie/Akun Terhapus...")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await cleaning_zombies.edit("Saya Tidak Memiliki Hak Blokir (Ban) Di Grup Ini.")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        stats = f"Dibersihkan `{del_u}` Zombies/Akun Terhapus"

    if del_a > 0:
        stats = f"Dibersihkan `{del_u}` Zombies/Akun Terhapus \
        \n`{del_a}` Akun Admin yang menjadi akun terhapus Tidak bisa Dihapus!"

    await cleaning_zombies.edit(stats)

@ALBY.on(events.callbackquery.CallbackQuery(data="zombies"))
async def _(event):
    await event.edit(CLEANER_HELP, buttons=[[Button.inline("« Kembali", data="help")]])
