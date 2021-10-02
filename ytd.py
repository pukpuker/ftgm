 #	#
#	#
#	#

# requires: pytube wget moviepy Pillow cryptg sponsorblock

import os
from .. import loader, utils
from telethon import events
from telethon.tl.types import Message, Channel
from moviepy.editor import VideoFileClip
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
	from moviepy.editor import VideoFileClip
	from pytube import YouTube
	from requests import get
	from io import BytesIO as IO
	import wget
	reply=await message.get_reply_message()
	url=reply.message
	yt=YouTube(url)
	thumb=wget.download(yt.thumbnail_url)
	name=yt.streams.filter(progressive=True).order_by('resolution').desc().first().download()
	
	clip=VideoFileClip(name)
	secs=clip.duration
	
	vvideo=await cutter(self, message, name, url, secs)
	
	await message.edit("uplovd")
	clip=VideoFileClip(name)
	secs=clip.duration
	await self.client.send_file(message.to_id, name, caption=f"<a href={url}>{yt.title}</a>", reply_to=reply, supports_streaming=True, duration=round(secs), thumb=thumb)
	os.remove(vvideo)
	os.remove(thumb)
	await message.delete()

async def cutter(self, message, name, url, secs):
	import sponsorblock as sb;import os
	cli = sb.Client()
	tet=True
	try:
		segments=cli.get_skip_segments(url)
	except:
		tet=False
	z=0;a=[]
	if tet!=False:
		from os import system as s
		segments.reverse()
		## oh shii*
		for _ in segments:
			s(f'ffmpeg -y -ss 0 -i "{name}" -to {_.start} -c copy "228.mp4"')
			s(f'ffmpeg -y -ss {_.end} -i "{name}" -to {secs} -c copy "337.mp4"')
			s(f'ffmpeg -y -i "concat:228.mp4|337.mp4" -c copy out.mp4')
			s(f"mv -f out.mp4 {name}")
		#return 'out.mp4'
	else:
		return tet
	#ae
