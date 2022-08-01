from typing import *
import random
from typing import Dict, List, Union

from ALBY import *
from telethon import *
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserNotParticipantError
)
from telethon.tl.types import PeerChannel,InputChannel
from telethon.tl.functions.channels import *
from telethon.tl.functions.channels import GetParticipantsRequest
from Config import Config
from telethon.tl.types import ChannelParticipantsSearch
import telethon
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import ExportChatInviteRequest


def AssistantAdd(mystic):
    async def wrapper(event):
        try:
            permissions = await event.client(GetParticipantRequest(int(event.chat_id), Config.ASSISTANT_ID))
        except UserNotParticipantError:
            if event.is_group:
                try:
                    link = await event.client(ExportChatInviteRequest(event.chat_id))
                    invitelinkk = link.link
                    invitelink = invitelinkk.replace(
                        "https://t.me/+", ""
                    )
                    await client(ImportChatInviteRequest(invitelink))
                    await event.reply(
                        f"Berhasil Bergabung",
                    )
                except UserAlreadyParticipantError:
                    pass
                except Exception as e:
                    await event.reply(
                        f"__Asisten Gagal Bergabung__\n\n**Reason**: {e}"
                    )
                    return
        return await mystic(event)

    return wrapper