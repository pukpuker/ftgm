from .. import loader, utils
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os, wget

def register(cb):
	cb(qdqdMod())
	
class qdqdMod(loader.Module):
	"""Обрезать медиа."""
	strings = {'name': 'qdqd'}
	
	async def ytcmd(self, msg):
		"""SSVDSDNKJBFNJ"""
		args = utils.get_args_raw(msg).split(':')
		reply = await msg.get_reply_message()
		if not reply or not reply.media:
			return await msg.edit('Нет реплая на медиа.')
		if args:
			if len(args)>1:
				skip=True if 'skip' in args[1] else False
			ag=args[0]
			if 'youtu' in ag:
				url=ag 
			else:
				url=reply.message
				skip=True if 'skip' in ag else False
		#return url, skip
		url=reply.message
		yt=YouTube(url)
		thumb=wget.download(yt.thumbnail_url)
		name=yt.streams.filter(progressive=True).order_by('resolution').desc().first().download()
		clip=VideoFileClip(name)
		secs=clip.duration
		c=0
		ext='.'+name.split('.')[-1]
		kek='kek'+ext
		kekk='kekk'+ext
		new='new'+ext
		import sponsorblock as sb;import os
		cli = sb.Client()
		try:segments=cli.get_skip_segments(url)
		except:
			await msg.reply(file=name, supports_streaming=True)
			os.system(f'rm -rf *{ext}')
			return await msg.delete()
		args=utils.get_args_raw(msg)#.split(',')
		from os import system as s
		segments.reverse
		for _ in segments:
			if round(_.start)<=1:
				os.system(f'ffmpeg -y -ss {_.end} -i "{name}" -to {secs} -c copy "seg_{str(c)+ext}"');c+=1

			elif round(_.end) != round(secs):
				os.system(f'ffmpeg -y -ss 0 -i "{name}" -to {_.start} -c copy "seg_{str(c)+ext}"');c+=1
				os.system(f'ffmpeg -y -ss {_.end} -i "{name}" -to {secs} -c copy "seg_{str(c)+ext}"');c+=1

			elif round(_.end) == round(secs):
				os.system(f'ffmpeg -y -ss 0 -i "{name}" -to {_.start} -c copy "seg_{str(c)+ext}"');c+=1


		open('inputs.txt','w').write('\n'.join(f"file seg_{i}{ext}" for i in range(0, c-1)))
		os.system(f'ffmpeg -y -f concat -i inputs.txt -c copy out.mp4')

		await msg.reply(file='out.mp4', supports_streaming=True)
		os.system(f'rm -rf *{ext}')
		#s(f'ffmpeg -y -i "concat:{228.mp4}|{kekk}" -c copy out.mp4')