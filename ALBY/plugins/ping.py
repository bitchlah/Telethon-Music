import os

from telethon import Button, events

from ALBY import *

IMG = os.environ.get(
    "PING_PIC", "https://telegra.ph/file/cbe826936d4de9ec1838a.jpg"
)
ms = 4

ALIVE = os.environ.get(
    "ALIVE", "@Punya_Alby"
)

CAPTION = f"**꧁•⊹٭Ping٭⊹•꧂**\n\n   ⚜ {ms}\n   ⚜ ❝𝐌𝐲 𝐌𝐚𝐬𝐭𝐞𝐫❞ ~『{ALIVE}』"


@ALBY.on(events.NewMessage(pattern="^/ping"))
async def _(event):
    UMM = [[Button.url("⚜ Cԋαɳɳҽʅ ⚜", "https://t.me/ruangprojects")]]
    await ALBY.send_file(event.chat_id, IMG, caption=CAPTION, buttons=UMM)
