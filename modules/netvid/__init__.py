import time

import vlc_player_compat as player
import threading
import os
import loading
import tempfile

class NetVid:
	TYPE_STRING='netvid'

	def __init__(self,queue,uid,url):
		self.player=player.Player()
		self.queue=queue
		self.uid=uid
		self.url=url
		self.duration=None
		self.time=None
		self.status='added'

	def get_url(self):
		return self.url

	def get_duration(self):
		return self.duration

	def get_time(self):
		return self.time

	def get_status(self):
		return self.time

	def play(self):
		self.show_loading_screen()
		if self.status=='invalid':
			return
		self.vidPlay()
		self.status='finishing'

	def show_loading_screen(self):
		self.loading_screen=loading.LoadingScreen()
		self.loading_screen.show()

	def hide_loading_screen(self):
		self.loading_screen.close()

	def pause(self):
		if self.status == 'paused':
			return
		if self.status != 'playing':
			raise Exception("Video is not playing")
		self.player.pause()
		self.status='paused'

	def stop(self):
		if self.status == 'stopped':
			return
		if not self.player.up():
			raise Exception("Video is not up")
		self.player.stop()
		self.status='stopped'

	def resume(self):
		if self.status == 'playing':
			return
		if self.status != 'paused':
			raise Exception("Video is not paused")
		self.player.play()
		self.status='playing'

	def vidPlay(self):
		self.player.load(self.url)

		self.status='loading'

		# Loop continuously, getting output and setting titles
		while self.player.up():
			time.sleep(0.1)
			duration=self.player.length()
			if duration is not None:
				if self.status=='loading':
					self.hide_loading_screen()
					self.status='playing'
				self.duration=duration
				self.time=self.player.time()
		self.player.stop()
		if self.cookies:
			os.unlink(self.cookies)

	def set_rate(self,rate):
		if not self.player.up():
			raise Exception("Cannot set rate of video that is not playing")
		self.player.set_rate(rate)

	def get_rate(self):
		if not self.player.up():
			return None
		return self.player.get_rate()

	# Class variables

	commands={
		'pause':pause,
		'resume':resume,
		'stop':stop,
		'set_rate':set_rate,
	}

	parameters={
		'url':get_url,
		'duration':get_duration,
		'status':get_status,
		'time':get_time,
		'rate':get_rate,
	}
