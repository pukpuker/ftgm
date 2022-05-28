# some text

from .. import loader, utils
import logging
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetFullChannelRequest

logger = logging.getLogger(__name__)


# https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
class E:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


@loader.tds
class userinfoMod(loader.Module):
    """Tells you about people"""

    common_list = {
            "id": "\nID: <code>{}</code>",
            "username": "\nUsername: <code>{}</code>",
            "scam": "\nScam: <code>{}</code>",
            "fake": "\nFake: <code>{}</code>"
    }
    general_list = {
            "first_name": "\nFirst name: <code>{}</code>",
            "last_name": "\nLast name: <code>{}</code>",
            "dc_id": "\nDC ID: <code>{}</code>",
            "bot": "\nBot: <code>{}</code>",
            "about": "\nBio: <code>{}</code>",
            "deleted": "\nDeleted: <code>{}</code>",
            "restricted": "\nRestricted: <code>{}</code>",
            "verified": "\nVerified: <code>{}</code>"
    }
    chat_list = {
            "location": "\nLocation: <code>{}</code>",
            "linked_chat_id": "\nLinked chat ID: <code>{}</code>",
            "title": "\nTitle: <code>{}</code>",
            "participants_count": "\nParticipants: <code>{}</code>",
            "date": "\nCreation date: <code>{}</code>",
            "megagroup": "\nMegagroup: <code>{}</code>",
            "gigagroup": "\nGigagroup: <code>{}</code>",
            "noforwards": "\nNo forwards: <code>{}</code>",
            "restriction_reason": "\nRestriction reason: <code>{}</code>"
    }
    strings = {
            "name": "userinfo",
            "find_error": "<b>Couldn't find that user.</b>",
            "no_args_or_reply": "<b>No args or reply was provided.</b>",
            "provide_user": "Provide a user to locate",
            "searching_user": "Searching for user...",
            "cannot_find": "Can't find user.",

            "permalink_txt": "<a href='tg://user?id={uid}'>\
                        {txt}</a>",

            "permalink_uid": "<a href='tg://user?id={uid}'>\
                        Permalink to {uid}</a>",

            "permalink_public_channel":
                "<a href='tg://resolve?domain={domain}'>\
                    Permalink to <code>{title}</code></a>",

            "permalink_private_channel":
                "<a href=\
                    'tg://privatepost?channel={channel_id}&post={post}'>\
                        Permalink1 to <code>{title}</code></a>(desktop)\
                        \n<a href=\
                            'tg://openmessage?chat_id={channel_id}'>\
                                Permalink2</a>(mobile)",

            "encode_cfg_doc": "Encode unicode characters"
    }

    def __init__(self):
        self.config = loader.ModuleConfig("ENCODE", False, lambda m: self.strings("encode_cfg_doc", m))
        self.replier = ''

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def humanize(self, list_, full, replier):
        for i in list_:
            l = getattr(full, i)
            if l not in [None, False, [], {}]:
                temp = list_[i].format(self._handle_string(l))
                if temp in replier: pass
                else: replier += temp

        self.replier += replier
        return

    async def get_user(self, message, args):
        m = await message.get_reply_message()
        if not(None is m):
            full = await self.client.get_entity(m.from_id)
        else:
            if not args:
                await utils.answer(message, self.strings("no_args_or_reply", message))
            try:
                if l := args[0]:
                    if '-100' in l: l = l[4:]
                    if l.isdigit(): entity = int(l)
                    else: entity = l

                full = await self.client.get_entity(entity)
            except Exception as e:
                logger.error(e)
                await utils.answer(
                    message,
                    self.strings("cannot_find", message))
        return full, m

    async def get_m(self, client, entity):
        res = await client.get_messages(
            await client.get_entity(entity), limit = 1)
        return res

    async def get_attributes(self, full):

        l = E(full.to_dict())
        if l._ == 'User':
            full = await self.client(GetFullUserRequest(l.id))
            obj = E(full.full_user.to_dict() | full.users[0].to_dict())

        elif l._ == 'Chat':
            full = await self.client(GetFullChatRequest(l.id))
            obj = E(full.full_chat.to_dict() | full.chats[0].to_dict())

        elif l._ == 'Channel':
            full = await self.client(GetFullChannelRequest(l.id))

            temp = {}; [temp.update(i.to_dict()) for i in full.chats]
            _ae = E(full.full_chat.to_dict() | temp)
            obj = E(full.full_chat.to_dict() | full.chats[0].to_dict())

        setattr(obj, 'dc_id', E(obj.photo).dc_id)

        return obj._, obj

    def _handle_string(self, string):
        if self.config["ENCODE"]:
            return utils.escape_html(ascii(string))
        return utils.escape_html(string)


    @loader.unrestricted
    @loader.ratelimit
    async def userinfocmd(self, message):
        """userinfo [username or id] insecure(optional flag, type if u want to show ur contact's name to others)"""

        args = utils.get_args(message)
        try:
            full, _m = await self.get_user(message, args)
            type_, full = await self.get_attributes(full)
        except Exception as e:
            logger.debug(e)
        # a little bit sesuritical
        if type_ == 'User' and not 'insecure' in args and message.chat and full.contact:
            full.first_name = None        #self._handle_string(full.first_name[0])
            try: full.last_name = None     #self._handle_string(full.last_name[0])
            except: pass
            full.phone = None             #self._handle_string(full.phone[0])
            self.hidden = True

        await self.humanize(self.common_list, full, '')
        if type_ == 'User':
            await self.humanize(self.general_list, full, '')
        if type_ == 'Chat':
            await self.humanize(self.chat_list, full, '')
        if type_ == 'Channel':
            await self.humanize(self.chat_list, full, '')

        await utils.answer(message, f'<u><b>{type_}</u> Info:</b>'+self.replier)

        # reset data
        self.replier = ''

    @loader.unrestricted
    @loader.ratelimit
    async def permalinkcmd(self, message):
        """Get permalink to user based on ID or username"""
        args = utils.get_args(message)
        full, _m = await self.get_user(message, args)
        l = E(full.to_dict())

        if l._ in ['Channel', 'Chat']:
            if l.username:
                await utils.answer(
                    message,
                    self.strings("permalink_public_channel",
                    message).format(
                        domain = l.username,
                        title = l.title))
            else:
                await utils.answer(
                    message,
                    self.strings("permalink_private_channel", message).format(
                                                        channel_id = l.id,
                                                        post = 2000001,
                                                        title = l.title))
        else:
            if len(args) > 1:
                await utils.answer(
                    message,
                    self.strings("permalink_txt", message).format(
                                                    uid = l.id,
                                                    txt = args[1]))
            else:
                await utils.answer(
                    message,
                    self.strings("permalink_uid", message).format(
                                                    uid = l.id))
