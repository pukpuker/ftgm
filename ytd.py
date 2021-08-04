#	#
#	#
#	#

# requires: pytube wget moviepy Pillow

import os
from .. import loader, utils
from telethon import events
from telethon.tl.types import Message, Channel
@loader.tds
class ytdlMod(loader.Module):
	"""yt downlod module"""
	strings = {
		"name": "ytdl"}

	def __init__(self):
		self.name = self.strings['name']
		
	async def client_ready(self, client, db):
		self.client = client
		self.db = db
	async def ytdcmd(self, message):
		""".ytd - dowmload yt video"""
		#os.system('pip uninstall Pillow -y && pip install Pillow')
		os.system("pip install Pillow pytube wget moviepy")
		reply=await message.get_reply_message()
		await ytd(self, message)

async def ytd(self, message):
	from pytube import YouTube
	from moviepy.editor import VideoFileClip
	from requests import get
	from io import BytesIO as IO
	import wget
	reply=await message.get_reply_message()
	url=reply.message
	yt=YouTube(url)
	thumb=wget.download(yt.thumbnail_url)
	vvideo=yt.streams.filter(progressive=True).order_by('resolution').desc().first().download()
	await message.edit("uplovd")
	await self.client.send_file(message.to_id, vvideo, caption=f"<a href={url}>{yt.title}</a>", reply_to=reply, supports_streaming=True, duration=round(yt.length), thumb=thumb)
	os.remove(vvideo)
	os.remove(thumb)
	await message.delete()