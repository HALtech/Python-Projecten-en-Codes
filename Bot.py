import discord
import logging
import os, sys
import time
import json
from PIL import Image
from subprocess import Popen
import urllib
import requests
import io
import urllib
#import telebot
import traceback
#import twitter
#import steam
#from steam.api import interface
import pyimgur
import asyncio
import imghdr
import sqlite3

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='Discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#UserName="kasper.ruhe@hotmail.com"
#Password="Salasanakissa-27"

#UserName="thebluekr@outlook.com"
#Password="Salasanakissa27"

Password = "MTY4NDYzNjA4NTgwMjc2MjI0.Cer_fw.iBVJPrHRMu1l2md5flOgfpOMdL8"

client = discord.Client()

#tb = telebot.TeleBot("205991125:AAGXay3xSfQX9DOC3mwbqyUUBUbJcoSyNN4")

CLIENT_ID = "f98c3d4ee47b0a6"
CLIENT_SECRET = "9b97d10373fa0b095808941427ed801ec2e3de03"
im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)

# api = twitter.Api(
				# consumer_key="9gsUF7JVl4A5kXU1g4LeMOlfC",
				# consumer_secret="uRaIGyOAkDahF7buB8joaaJ81dPMjzHCgbgG1z5FOTHlL2ObE9",
				# access_token_key="436702863-KLCi2AoJB1ZhBlWHNW50gktv8qiKgx199YcsFLHN",
				# access_token_secret="otK9HEvIPuLZGCYHGeJ8uOEf3YWrQlQ98i6LehE5Gqt02")

OwnerID = ["121546822765248512"]
BotID = ["138365437791567872"]

RadioList = []

Variables = []

VoteStart = 0
VotedString = []
VoteString = []
VoteListString = []
VoteType = 0
PollContent = []
PollContentString = []
VoteOptionString = []

TimeString = 3600

Connected  = 0

try:
	with open('./Settings/Gags.json', 'r') as GagFile:
		GagList = json.load(GagFile)
except:
	with open('./Settings/Gags.json', 'w') as GagFile:
		GagList = []

try:
	with open('./Settings/LogChannel.json', 'r') as LogFile:
		LogChannel = json.load(LogFile)
except:
	with open('./Settings/LogChannel.json', 'w') as LogFile:
		LogChannel = ["176797996640501760","138365437791567872"]
		print('An error has occured during setting up a logging Channel, please change the json file inside the Variables directory\nThe id for a Channel can be received using channelid and serverid\nMake sure to copy the id displayed inside the message to the clipboard and paste it in the LogChannel.json file between the ""\nUsing now the standard values')

try:
	with open('./Settings/Channels.json', 'r') as ChannelFile:
		Channels = json.load(ChannelFile)
except:
	with open('./Settings/Channels.json', 'w') as ChannelFile:
		Channels = []

try:
	with open('./Settings/Game.json', 'r') as GameFile:
		StringGame = json.load(GameFile)
except:
	with open('./Settings/Game.json', 'w') as GameFile:
		StringGame = ["Discord.py's great migration","http://www.twitch.tv/logout",0]

try:
	with open('./Settings/Panel.json', 'r') as PanelFile:
		PanelUser = json.load(PanelFile)
except:
	with open('./Settings/Panel.json', 'w') as PanelFile:
		PanelUser = ["121546822765248512"]
		
try:
	with open('./Settings/PlayList.json', 'r') as PlayListFile:
		RadioList = json.load(PlayListFile)
except:
	with open('./Settings/PlayList.json', 'w') as PlayListFile:
		RadioList = []
		
try:
	with open('./Settings/Note.json', 'r') as NoteFile:
		Note = json.load(PlayListFile)
except:
	with open('./Settings/Note.json', 'w') as NoteFile:
		Note = []

try:
	with open('./Settings/Radio.json', 'r') as RadioFile:
		VoiceChannelID = json.load(RadioFile)
except:
	with open('./Settings/Radio.json', 'w') as RadioFile:
		VoiceChannelID = ""

try:
	with open('./Settings/BannedSounds.json', 'r') as SoundFile:
		BanSound = json.load(SoundFile)
except:
	with open('./Settings/BannedSounds.json', 'w') as SoundFile:
		BanSound = []

@client.async_event
def on_ready():
	print("Logged in as '{}'".format(client.user.name))
	Game = discord.Game()
	Game.name = StringGame[0]
	Game.url = StringGame[1]
	Game.type = StringGame[2]
	yield from asyncio.sleep(1)
	yield from client.change_status(game=Game)
	print("Playing now: '{}'".format(StringGame[0]))
	print("Stream link: '{}'".format(StringGame[1]))
	if StringGame[2] == 0:
		print("Streaming mode: False")
	else:
		print("Streaming mode: True")
	if "" in GagList:
		GagList.remove("")
	try:
		print("Loaded {} gagged users".format(len(GagList)))
		print("Loaded {} permitted channels".format(len(Channels)))
		print("Loaded {} songs in the playlist".format(len(RadioList)))
		print("Logging Channel: {0}\nLogging Server: {1}".format(client.get_channel(LogChannel[0]),client.get_server(LogChannel[1])))
		yield from client.send_message(client.get_channel(LogChannel[0]), "Loaded {} gagged users".format(len(GagList)))
		yield from client.send_message(client.get_channel(LogChannel[0]), "Loaded {} permitted channels".format(len(Channels)))
		yield from client.send_message(client.get_channel(LogChannel[0]), "```Logging settings\nLogging Server: {1}\nLogging Channel: {0}```".format(client.get_channel(LogChannel[0]),client.get_server(LogChannel[1])))
		try:
			global voice
			voice = yield from client.join_voice_channel(client.get_channel(VoiceChannelID))
			print("Joined voice channel: {}".format(voice.channel.name))
		except:
			print("Voicechannel not registed in config")
	except:
		print("Error sending messages to the logging Channel")
	global DataBase
	global Cursor
	if os.path.isfile("./Database/Points.db") == True:
		Database = sqlite3.connect('./Database/Points.db')
		Cursor = Database.cursor()
		print("Succesfully loaded the Points database")
	else:
		Database = sqlite3.connect('./Database/Points.db')
		print("Creating Points database")
		Cursor = Database.cursor()
		Cursor.execute('CREATE TABLE POINTS (ID INT PRIMARY KEY NOT NULL, AMOUNT INT NOT NULL);')

@client.async_event
def on_member_join(member):
	yield from client.send_message(member.server.default_channel,"Welcome {0} to {1}".format(member.name,member.server.name))

@client.async_event
def on_message(msg):
	try:
		try:
			try:
				for gag in GagList:
					if msg.author.id in GagList:
						yield from client.delete_message(msg)
						break
			except:
				pass
			if msg.raw_mentions[0] == client.user.id:
				global Message
				Message = msg.content
				Message = Message.split(" ")
				del Message[0]
				Message = " ".join(Message)
				
				global MessageID
				MessageID = msg.raw_mentions
				del MessageID[0]
				
				if Message.startswith("invite"):
					InviteString = discord.utils.oauth_url("168460881599004672")
					print(InviteString)
					yield from client.send_message(msg.channel, "Invite URL: {}".format(InviteString))
					
				elif Message.startswith("play "):
					Message = Message.split(" ")
					del Message[0]
					global BanSound
					if Message[0] == "dir":
						del Message[0]
						if Message:
							if Message[0] in BanSound:
								pass
							else:
								PlayDir = os.listdir("./Sounds/{}".format(Message[0]))
								yield from client.send_message(msg.channel, "Directory: ```{}```".format(" | ".join(PlayDir[0:50])))
								del PlayDir[0:50]
								yield from asyncio.sleep(1)
								while (len(PlayDir)>=1):
									yield from client.send_message(msg.channel, "```{}```".format(" | ".join(PlayDir[0:50])))
									del PlayDir[0:50]
									yield from asyncio.sleep(2.5)
						elif not Message:
							if Message in BanSound:
								pass
							else:
								PlayDir = os.listdir("./Sounds/")
								yield from client.send_message(msg.channel, "Directory: ```{}```".format(" | ".join(PlayDir[0:50])))
								del PlayDir[0:50]
								yield from asyncio.sleep(1)
								while (len(PlayDir)>=1):
									yield from client.send_message(msg.channel, "```{}```".format(" | ".join(PlayDir[0:50])))
									del PlayDir[0:50]
									yield from asyncio.sleep(2.5)
					elif Message[0] == "disable":
						del Message[0]
						if Message:
							if Message[0].endswith(".mp3"):
								PlayBoolean = os.path.exists("./Sounds/{}".format(Message[0]))
								PlayDir = Message[0]
								if PlayBoolean == True:
									if PlayDir in BanSound:
										pass
									else:
										BanSound.append(PlayDir)
								else:
									pass
							else:
								PlayBoolean = os.path.isdir("./Sounds/{}".format(Message[0]))
								PlayDir = Message[0]
								if PlayBoolean == True:
									if PlayDir in BanSound:
										pass
									else:
										BanSound.append(PlayDir)
								else:
									pass
					elif Message[0] == "enable":
						del Message[0]
						if Message:
							if Message[0].endswith(".mp3"):
								PlayBoolean = os.path.exists("./Sounds/{}".format(Message[0]))
								PlayDir = Message[0]
								if PlayBoolean == True:
									if PlayDir in BanSound:
										BanSound.remove(PlayDir)
									else:
										pass
								else:
									pass
							else:
								PlayBoolean = os.path.isdir("./Sounds/{}".format(Message[0]))
								PlayDir = Message[0]
								if PlayBoolean == True:
									if PlayDir in BanSound:
										BanSound.remove(PlayDir)
									else:
										pass
								else:
									pass
					else:
						if msg.author.id in OwnerID:
							if voice.is_connected() == True:
								global soundplayer
								try:
									if player.is_playing() == False:
										try:
											if soundplayer.is_playing() == False:
												Message = " ".join(Message)
												Message = "./Sounds/" + Message
												soundplayer = voice.create_ffmpeg_player(Message)
												soundplayer.start()
											else:
												soundplayer.stop()
												Message = " ".join(Message)
												Message = "./Sounds/" + Message
												soundplayer = voice.create_ffmpeg_player(Message)
												soundplayer.start()
										except NameError:
											Message = " ".join(Message)
											Message = "./Sounds/" + Message
											soundplayer = voice.create_ffmpeg_player(Message)
											soundplayer.start()
									else:
										pass
								except NameError:
									try:
										if soundplayer.is_playing() == False:
											Message = " ".join(Message)
											Message = "./Sounds/" + Message
											soundplayer = voice.create_ffmpeg_player(Message)
											soundplayer.start()
										else:
											soundplayer.stop()
											Message = " ".join(Message)
											Message = "./Sounds/" + Message
											soundplayer = voice.create_ffmpeg_player(Message)
											soundplayer.start()
									except NameError:
										Message = " ".join(Message)
										Message = "./Sounds/" + Message
										soundplayer = voice.create_ffmpeg_player(Message)
										soundplayer.start()
							else:
								yield from client.send_message(msg.channel, "Not connected to voicechannel")
						else:
							if Message[0] in BanSound:
								pass
							else:
								if voice.is_connected() == True:
									global soundplayer
									try:
										if player.is_playing() == False:
											try:
												if soundplayer.is_playing() == False:
													Message = " ".join(Message)
													Message = "./Sounds/" + Message
													soundplayer = voice.create_ffmpeg_player(Message)
													soundplayer.start()
												else:
													soundplayer.stop()
													Message = " ".join(Message)
													Message = "./Sounds/" + Message
													soundplayer = voice.create_ffmpeg_player(Message)
													soundplayer.start()
											except NameError:
												Message = " ".join(Message)
												Message = "./Sounds/" + Message
												soundplayer = voice.create_ffmpeg_player(Message)
												soundplayer.start()
										else:
											pass
									except NameError:
										try:
											if soundplayer.is_playing() == False:
												Message = " ".join(Message)
												Message = "./Sounds/" + Message
												soundplayer = voice.create_ffmpeg_player(Message)
												soundplayer.start()
											else:
												soundplayer.stop()
												Message = " ".join(Message)
												Message = "./Sounds/" + Message
												soundplayer = voice.create_ffmpeg_player(Message)
												soundplayer.start()
										except NameError:
											Message = " ".join(Message)
											Message = "./Sounds/" + Message
											soundplayer = voice.create_ffmpeg_player(Message)
											soundplayer.start()
								else:
									yield from client.send_message(msg.channel, "Not connected to voicechannel")
						

				elif Message.startswith("error"):
					raise Exception

				elif Message.startswith("myid"):
					yield from client.send_message(msg.channel, msg.author.id)

				elif Message.startswith("userid"):
					del MessageID[0]
					IdList = "Tagged users: "+ " | ".join(MessageID)
					yield from client.send_message(msg.channel, IdList)
					print(IdList)
				
				elif Message.startswith("channelid"):
					yield from client.send_message(msg.channel, "Channel ID: {}".format(msg.channel.id))

				elif Message.startswith("serverid"):
					yield from client.send_message(msg.channel, "Server ID: {}".format(msg.server.id))
				
				elif Message.startswith("note "):
					if msg.author.id in OwnerID:
						Message = Message.split(" ")
						del Message[0]
						if Message[0] == "add":
							del Message[0]
							member = discord.utils.get(msg.server.members, name=Message[0])
							if member is None:
								yield from client.send_message(msg.channel, "User not found")
							else:
								NoteMember = str(member.id)
								del NoteUser[0]
								NoteUser = " ".join(NoteUser)
								global Note
								NoteMember = NoteMember.split(" ")
								NoteMember.append(NoteUser)
								Note.append(NoteMember)
								print(NoteUser)
								print(NoteMember)
								print(Note)
								print(Note.index(str(member.id)))
						elif Message[0] == "display":
							del Message[0]
							member = discord.utils.get(msg.server.members, name=Message[0])
							if member is None:
								yield from client.send_message(msg.channel, "User not found")
							else:
								NoteMember = str(member)
								NoteMember = NoteMember.split("#")
								del NoteMember[0]
								NoteMember = " ".join(NoteMember)
								del NoteUser[0]
								NoteUser = " ".join(NoteUser)
								print(Note[int(NoteMember)])
				
				elif Message.startswith("points "):
					Message = Message.split(" ")
					del Message[0]
					Message = " ".join(Message)
					if Message.startswith("display"):
						Cursor.execute("SELECT ID FROM POINTS WHERE ID=?", (msg.author.id,))
						returnObject = Cursor.fetchone()
						print(returnObject)
						if returnObject:
							yield from client.send_message(msg.channel, returnObject[0])
					elif Message.startswith("add"):
						if msg.author.id in OwnerID:
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							Cursor.execute("UPDATE POINTS SET AMOUNT = AMOUNT + ? WHERE ID=?", (int(Message),msg.author.id,))
							yield from client.send_message(msg.channel, "Amount increased by {0}".format(Message))
				
				elif Message.startswith("whois "):
					Owner = msg.server.owner
					Message = Message.split(" ")
					del Message[0]
					if len(MessageID) == 1:
						member = discord.utils.get(msg.server.members, id=MessageID[0])
						createdate = str(member.created_at)
						createdate = createdate.split(".")
						del createdate[1]
						createdate = "".join(createdate)
						joindate = str(member.joined_at)
						joindate = joindate.split(".")
						del joindate[1]
						joindate = "".join(joindate)
						yield from client.send_message(msg.channel, "```Name: {0}\nID: {1}\nDisplayed name: {2}\nStatus: {3}\nBot account: {4}\nCreation date: {5}\nJoin date: {6}\nAFK: {7}```".format(member.name, member.id, member.display_name, member.status, member.bot, createdate, joindate, member.is_afk))
					elif len(MessageID) == 0:
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						member = discord.utils.get(msg.server.members, name=Message)
						if member is None:
							yield from client.send_message(msg.channel, "User not found")
						else:
							createdate = str(member.created_at)
							createdate = createdate.split(".")
							del createdate[1]
							createdate = "".join(createdate)
							joindate = str(member.joined_at)
							joindate = joindate.split(".")
							del joindate[1]
							joindate = "".join(joindate)
							if member.id == Owner.id:
								yield from client.send_message(msg.channel, "```Name: {0}\nID: {1}\nDisplayed name: {2}\nStatus: {3}\nBot account: {4}\nCreation date: {5}\nJoin date: {6}\nAFK: {7}\nSpecial notes: Owner```".format(member.name, member.id, member.display_name, member.status, member.bot, createdate, joindate, member.is_afk))
							else:
								yield from client.send_message(msg.channel, "```Name: {0}\nID: {1}\nDisplayed name: {2}\nStatus: {3}\nBot account: {4}\nCreation date: {5}\nJoin date: {6}\nAFK: {7}```".format(member.name, member.id, member.display_name, member.status, member.bot, createdate, joindate, member.is_afk))

				elif Message.startswith("clean "):
					if msg.author.id in OwnerID:
						Message = Message.split(" ")
						if len(Message) == 2:
							del Message[0]
							Message = " ".join(Message)
							try:
								Number = int(Message)+1
								yield from client.purge_from(msg.channel, limit=Number)
							except TypeError:
								yield from client.send_message(msg.channel, "Invalid number given")
				
				elif Message.startswith("dj "):
					if msg.author.id in OwnerID:
						DjContent = Message
						DjContent = DjContent.split(" ")
						del DjContent[0]
						DjContent = " ".join(DjContent)
						if DjContent.startswith("add"):
							Dj = msg.raw_mentions
							if len(Dj) == 1:
								if Dj in PanelUser:
									pass
								else:
									global PanelUser
									Dj = " ".join(Dj)
									PanelUser.append(Dj)
									print(PanelUser)
									yield from client.send_message(msg.channel, "Succesfully added {0}".format(msg.mentions[1].name))
						elif DjContent.startswith("remove"):
							Dj = msg.raw_mentions
							if len(Dj) == 1:
								if Dj in PanelUser:
									global PanelUser
									Dj = " ".join(Dj)
									PanelUser.remove(Dj)
									print(PanelUser)
									yield from client.send_message(msg.channel, "Succesfully removed {0}".format(msg.mentions[1].name))
								else:
									pass
				
				elif Message.startswith("radio "):
					if msg.author.id in PanelUser:
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						if Message.startswith("setup"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							global channel
							channel = discord.utils.get(msg.server.channels, name=Message, type=discord.ChannelType.voice)
							global voice
							global VoiceChannelID
							try:
								if voice.is_connected() == True:
									yield from voice.disconnect()
									voice = yield from client.join_voice_channel(channel)
									VoiceChannelID = voice.channel.id 
								else:
									voice = yield from client.join_voice_channel(channel)
									VoiceChannelID = voice.channel.id
							except NameError:
								voice = yield from client.join_voice_channel(channel)
								VoiceChannelID = voice.channel.id
						elif Message.startswith("quit"):
							try:
								yield from voice.disconnect()
								player.stop()
							except:
								pass
						elif Message.startswith("add"):
							Message = Message.split(" ")
							del Message[0]
							if len(Message) == 1:
								Message = " ".join(Message)
								global RadioList
								RadioList.append(Message)
								yield from client.send_message(msg.channel, "Succesfully added song to list")
						elif Message.startswith("skip"):
							player.stop()
							yield from client.send_message(msg.channel, "Skipping `{0}`".format(player.title))
						elif Message.startswith("play"):
							if len(RadioList) >= 1:
								if voice.is_connected() == True:
									while (len(RadioList) >= 1):
										global player
										player = yield from voice.create_ytdl_player(str(RadioList[0]))
										player.start()
										Duration = time.strftime('%H:%M:%S', time.gmtime(player.duration))
										yield from client.send_message(msg.channel, "Started playing: \n```Title: {0}\nDuration: {1}\nViews: {2}```".format(player.title,Duration,player.views))
										Game = discord.Game()
										Game.name = player.title
										Game.type = 1
										Game.url = "https://www.twitch.tv/logout"
										yield from client.change_status(game=Game)
										yield from asyncio.sleep(1)
										while (player.is_done() == False):
											yield from asyncio.sleep(1)
										else:
											player.stop()
											global RadioList
											del RadioList[0]
											yield from asyncio.sleep(1)
									else:
										yield from asyncio.sleep(1)
										Game = discord.Game()
										Game.name = StringGame[0]
										Game.url = StringGame[1]
										Game.type = StringGame[2]
										yield from client.change_status(game=Game)
						elif Message.startswith("stop"):
							player.stop()
							del RadioList[0]
							yield from asyncio.sleep(2)
							Game = discord.Game()
							Game.name = StringGame
							yield from client.change_status(game=Game)
						elif Message.startswith("pause"):
							player.pause()
						elif Message.startswith("resume"):
							player.resume()
						elif Message.startswith("volume"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							try:
								Volume = float(Message)
								if 0 <= Volume <= 10:
									Volume = Volume/5
									Volume = "%0.1f" % Volume
									player.volume = float(Volume)
								else:
									yield from client.send_message(msg.channel, "Keep volume between `0` and `10`")
							except:
								yield from client.send_message(msg.channel, "Keep volume between `0` and `10`")
						elif Message.startswith("help"):
							yield from client.send_message(msg.channel, "Current commands:\n```add\nplay\nstop\nskip\nvolume```")
				
				elif Message.startswith("player"):
					if msg.author.id in PanelUser:
						Message = Message.split(" ")
						Message[0] = "radio"
						Message = " ".join(Message)
						yield from client.send_message(msg.channel, "You possibly ment `{0}` instead of `{1}`".format(Message,msg.content))
				
				elif Message.startswith("addchannel"):
					if msg.author.id in OwnerID:
						if msg.channel.id in Channels:
							yield from client.send_message(msg.channel, "This channel is already added")
						else:
							global Channels
							yield from client.send_typing(msg.channel)
							Channels.append(msg.channel.id)
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							if "-silent" in Message:
								print("Succesfully registed `{0}` as permitted channel".format(msg.channel.name))
							else:
								yield from client.send_message(msg.channel,"Succesfully registed `{0}` as permitted channel".format(msg.channel.name))
				
				elif Message.startswith("remchannel"):
					if msg.author.id in OwnerID:
						if msg.channel.id in Channels:
							yield from client.send_message(msg.channel, "This channel isn't in the list")
						else:
							global Channels
							yield from client.send_typing(msg.channel)
							Channels.remove(msg.channel.id)
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							if "-silent" in Message:
								print("Succesfully unregisted `{0}` as permitted channel".format(msg.channel.name))
							else:
								yield from client.send_message(msg.channel,"Succesfully unregisted `{0}` as permitted channel".format(msg.channel.name))

				elif Message.startswith("game "):
					if msg.author.id in OwnerID:
						yield from client.send_typing(msg.channel)
						global StringGame
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						StringGame[0] = Message
						game = discord.Game()
						game.name = StringGame[0]
						game.url = StringGame[1]
						game.type = StringGame[2]
						yield from client.change_status(game=game)
						if StringGame[2] == 0:
							print("Playing now: "+StringGameContent)
							yield from client.send_message(msg.channel, "Playing now: `{}`".format(StringGameContent))
							yield from client.send_message(client.get_channel(LogChannel[0]), "Playing now: `{}`".format(StringGameContent))
						else:
							print("Streaming now: "+StringGameContent)
							yield from client.send_message(msg.channel, "Streaming now: `{}`".format(StringGameContent))
							yield from client.send_message(client.get_channel(LogChannel[0]), "Streaming now: `{}`".format(StringGameContent))
				
				elif Message.startswith("stream "):
					if msg.author.id in OwnerID:
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						global StringGame
						if Message.startswith("mode"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							try:
								StringGame[2] = int(Message)
								game = discord.Game()
								game.name = StringGame[0]
								game.url = StringGame[1]
								game.type = StringGame[2]
								yield from client.change_status(game=game)
							except:
								yield from client.send_message(msg.channel, "Given input isn't number")
						elif Message.startswith("url"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							StringGame[1] = Message
							game = discord.Game()
							game.name = StringGame[0]
							game.url = StringGame[1]
							game.type = StringGame[2]
							yield from client.change_status(game=game)
				
				elif Message.startswith("gag"):
					if msg.author.id in OwnerID:
						yield from client.send_typing(msg.channel)
						if len(MessageID) == 1:
							member = discord.utils.get(msg.server.members, id=MessageID[0])
							if MessageID[0] not in GagList:
								global GagList
								GagList.append(MessageID[0])
								yield from client.send_message(msg.channel, "Gagged {}".format(member.name))
							else:
								yield from client.send_message(msg.channel, "{} is already gagged".format(member.name))
							
				elif Message.startswith("ungag"):
					if msg.author.id in OwnerID:
						yield from client.send_typing(msg.channel)
						if len(MessageID) == 1:
							member = discord.utils.get(msg.server.members, id=MessageID[0])
							if MessageID[0] in GagList:
								global GagList
								GagList.remove(MessageID[0])
								yield from client.send_message(msg.channel, "Ungagged {}".format(member.name))
							else:
								yield from client.send_message(msg.channel, "{} isn't gagged".format(member.name))

				elif Message.startswith("shutdown"):
					if msg.author.id in OwnerID:
						try:
							if voice.is_connected() == True:
								yield from voice.disconnect()
								yield from client.logout()
							else:
								yield from client.logout()
						except:
							yield from client.logout()
				
				elif Message.startswith("config "):
					if msg.author.id in OwnerID:
						global LogChannel
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						if Message.startswith("channel"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							ConfigChannelString = client.get_channel(Message)
							if ConfigChannelString:
								LogChannel[0] = Message
								yield from client.send_message(msg.channel, "Succesfully changed to {}".format(ConfigChannelString))
							else:
								yield from client.send_message(msg.channel, "The given ID isn't valid")
						elif Message.startswith("server"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							ConfigServerString = client.get_server(Message)
							if ConfigServerString:
								LogChannel[1] = Message
								yield from client.send_message(msg.channel, "Succesfully changed to {}".format(ConfigServerString))
							else:
								yield from client.send_message(msg.channel, "The given ID isn't valid")
						elif Message.startswith("setup"):
							LogChannel[0] = msg.channel.id
							LogChannel[1] = msg.server.id
							yield from client.send_message(msg.channel, "Succesfully configurated this Server and Channel for logging")
							yield from client.send_message(msg.channel, "```Logging settings\nServer: {0}\nChannel: {1}```".format(client.get_server(LogChannel[1]),client.get_channel(LogChannel[0])))
						elif Message.startswith("list"):
							yield from client.send_message(msg.channel, "```Logging settings\nServer: {0}\nChannel: {1}```".format(client.get_server(LogChannel[1]),client.get_channel(LogChannel[0])))
						else:
							yield from client.send_message(msg.channel, "Use the following formats to change the Channel and Server IDs\n```config Channel <id>\nconfig Server <id>\nconfig Setup\nconfig List```")

				elif Message.startswith("rename "):
					if msg.author.id in OwnerID:
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						yield from client.send_typing(msg.channel)
						yield from client.edit_profile(username=Message)
						yield from client.send_message(msg.channel, "Renamed to: '{}'".format(Message))
						yield from client.send_message(client.get_channel(LogChannel[0]), "Renamed to: '{}'".format(Message))
					
				elif Message.startswith("picture "):
					if msg.author.id in OwnerID:
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						if Message.startswith("imgur"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							if len(Message) == 24:
								Message = Message.split("/")
								del Message[0:3]
								Message = " ".join(Message)
								image = im.get_image(Message)
								image.download(path="./Pictures/",name="Avatar",overwrite=True)
								yield from asyncio.sleep(1)
								ImageFormat = image.type
								ImageFormat = ImageFormat.split("/")
								del ImageFormat[0]
								ImageFormat = " ".join(ImageFormat)
								if ImageFormat == "jpg":
									with open('./Pictures/Avatar.jpg', 'rb') as ProfileImage:
										Avatar = ProfileImage.read()
										yield from client.edit_profile(Password,avatar=Avatar)
								elif ImageFormat == "png":
									with open('./Pictures/Avatar.png', 'rb') as ProfileImage:
										Avatar = ProfileImage.read()
										yield from client.edit_profile(Password,avatar=Avatar)
								elif ImageFormat == "jpeg":
									with open('./Pictures/Avatar.jpg', 'rb') as ProfileImage:
										Avatar = ProfileImage.read()
										yield from client.edit_profile(Password,avatar=Avatar)
								else:
									yield from client.send_message(msg.channel, "Image type not supported\nFormat used is `{}`".format(ImageFormat))
						elif Message.startswith("storage"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							if Message.startswith("jpg"):
								with open('Avatar.jpg', 'rb') as ProfileImage:
									Avatar = ProfileImage.read()
									yield from client.edit_profile(Password,avatar=Avatar)
							elif Message.startswith("png"):
								with open('Avatar.png', 'rb') as ProfileImage:
									Avatar = ProfileImage.read()
									yield from client.edit_profile(Password,avatar=Avatar)
						elif Message.startswith("default"):
							with open("Default.png", "rb") as ProfileImage:
								Avatar = ProfileImage.read()
								yield from client.edit_profile(Password,avatar=Avatar)
				
				elif Message.startswith("nick"):
					if msg.author.id in OwnerID:
						yield from client.send_typing(msg.channel)
						Message = Message.split(" ")
						del Message[0]
						Message = " ".join(Message)
						if len(Message) >= 1:
							yield from client.change_Message(msg.server.me, Message)
							yield from client.send_message(msg.channel, "Message changed to: `{0}`".format(Message))
							yield from client.send_message(client.get_channel(LogChannel[0]), "Message changed to: `{0}`\nServer: `{1}`".format(Message,msg.server.name))
						else:
							yield from client.change_Message(msg.server.me, Message)
							yield from client.send_message(msg.channel, "Removed Message".format(Message))
							yield from client.send_message(client.get_channel(LogChannel[0]), "Removed Message\nServer: `{1}`".format(Message,msg.server.name))

				if msg.channel.id in Channels:
					if msg.author.id in GagList:
						pass
					else:
						if Message.startswith("shrug"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "¯\\_(ツ)\_/¯")
						elif Message.startswith("bomb"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "●～*")
						elif Message.startswith("flip"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "(╯°□°）╯︵ ┻━┻")
						elif Message.startswith("unflip"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "┬─┬ノ( º _ ºノ)")
						elif Message.startswith("bear"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "ʕ•ᴥ•ʔ")
						elif Message.startswith("lenny"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "( ͡° ͜ʖ ͡°)")
						elif Message.startswith("givebot"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "つ ◕\_◕ ༽つ Give bots perms ༼ つ ◕\_◕ ༽つ")
						elif Message.startswith("starfish"):
							yield from client.send_typing(msg.channel)
							yield from client.send_message(msg.channel, "ヽ༼ຈل͜ຈ༽ﾉ GIVE STARFISH PROMOTION or RIOT ヽ༼ຈل͜ຈ༽ﾉ")
						elif Message.startswith("c-riot"):
							yield from client.send_typing(msg.channel)
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							print("Sending '{}' riot".format(Message))
							yield from client.send_message(msg.channel, "{0}: ヽ༼ຈل͜ຈ༽ﾉ {1} ヽ༼ຈل͜ຈ༽ﾉ".format(msg.author.name, Message))
							yield from client.send_message(client.get_channel(LogChannel[0]), "{0}: Custom Riot `{1}`".format(msg.author.name, Message))
						
						elif Message.startswith("c-give"):
							yield from client.send_typing(msg.channel)
							GiveString = Message
							GiveString = GiveString.split(" ")
							del GiveString[0]
							GiveString = " ".join(GiveString)
							yield from client.send_message(msg.channel, "{0}: ༼ つ ◕\_◕ ༽つ {1} ༼ つ ◕\_◕ ༽つ".format(msg.author.name, GiveString))

						elif Message.startswith("nsfl"):
							yield from client.send_typing(msg.channel)
							marquee = yield from client.send_message(msg.channel, "``` ```")
							yield from client.send_typing(msg.channel)
							time.sleep(0.75)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ```")
							yield from client.send_typing(msg.channel)
							time.sleep(0.75)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ              ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ N            ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NS           ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSF          ヽ༼ຈل͜ຈ༽ﾉ```")
							yield from client.send_typing(msg.channel)
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL         ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL o       ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL or      ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL or R    ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL or RI   ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL or RIO  ヽ༼ຈل͜ຈ༽ﾉ```")
							time.sleep(0.5)
							yield from client.edit_message(marquee , "```ヽ༼ຈل͜ຈ༽ﾉ NSFL or RIOT ヽ༼ຈل͜ຈ༽ﾉ```")

						elif Message.startswith("list"):
							yield from client.send_message(msg.channel, GagList)
						
						# elif Message.startswith("tweet"):
							# if msg.author.id in OwnerID:
								# yield from client.send_typing(msg.channel)
								# TweetString = Message
								# TweetString = TweetString.replace("tweet"+" ", "")
								# if len(TweetString) <= 140:
									# twitter.api.Api.PostUpdate(api,status=TweetString)
									# yield from client.send_message(client.get_channel(LogChannel[0]), "Sending tweet: `{}`".format(TweetString))
								# else:
									# yield from client.send_message(msg.channel, "Tweet extended the character limit by `{}`".format(len(TweetString)-140))
						
						elif Message.startswith("eval"):
							if msg.author.id in OwnerID:
								yield from client.send_typing(msg.channel)
								Message = Message.split(" ")
								del Message[0]
								Message = " ".join(Message)
								try:
									yield from client.send_message(msg.channel, '```{}```'.format(eval(Message)))
								except Exception as ExecuteFail:
									yield from client.send_message(msg.channel, "Error:\n```{}```".format(ExecuteFail))
									yield from client.send_message(client.get_channel(LogChannel[0]), "Error:\n```{}```".format(ExecuteFail))

						elif Message.startswith("bot.exe"):
							if msg.author.id in OwnerID:
								yield from client.send_typing(msg.channel)
								Message = Message.split(" ")
								del Message[0]
								Message = " ".join(Message)
								yield from client.send_message(client.get_channel(LogChannel[0]), "BlueBot: `client.send_message(msg.channel, {}`".format(Message))
								yield from client.send_message(msg.channel, "{}".format(Message))

						elif Message.startswith("poll "):
							if msg.author.id in OwnerID:
								global PollContent
								PollContent = []
								global VoteOptionString
								VoteOptionString = []
								global PollContentString
								PollContentString = Message
								PollContentString = PollContentString.split(" ")
								del PollContentString[0]
								PollContentString = " ".join(PollContentString)
								if PollContentString == "":
									yield from client.send_message(msg.channel, "No input found")
								elif PollContentString.startswith("time"):
									PollContentString = PollContentString.split(" ")
									del PollContentString[0]
									PollContentString = " ".join(PollContentString)
									if PollContentString.startswith("set"):
										PollContentString = PollContentString.split(" ")
										del PollContentString[0]
										PollContentString = " ".join(PollContentString)
										if int(PollContentString) == TimeString:
											global TimeString
											TimeString = int(PollContentString)
											yield from client.send_message(msg.channel, "Time has been set to: `{}`".format(TimeString))
										else:
											yield from client.send_message(msg.channel, "The time has already been configured to that")
									elif PollContentString.startswith("display"):
										yield from client.send_message(msg.channel, "Current time is set to `{}`".format(TimeString))
								else:
									if "-" in PollContentString:
										global CountVote
										CountVote = 0
										while (len(PollContentString) > 1):
											if PollContentString.startswith("-"):
												if len(PollContentString) == 1:
													VoteOptionString.append(PollContentString)
													CountVote += 1
													del PollContentString
												else:
													PollContentString = PollContentString.split()
													VoteOptionString.append(PollContentString[0])
													del PollContentString[0]
													PollContentString = " ".join(PollContentString)
											else:
												if len(PollContentString) == 1:
													PollContent.append(PollContentString)
													del PollContentString
												else:
													PollContentString = PollContentString.split()
													PollContent.append(PollContentString[0])
													del PollContentString[0]
													PollContentString = " ".join(PollContentString)
										print("Found tags")
										if VoteStart == 0:
											global VoteStart
											VoteStart = 1
											global VotedString
											VotedString = []
											global VoteString
											VoteString = []
											global VoteListString
											VoteListString = []
											global VoteType
											VoteType = 1
											yield from client.send_typing(msg.channel)
											yield from client.send_message(msg.channel, "Started poll:\n```{}```\nTo vote type `vote <number>`".format(" ".join(PollContent)))
											VoteOptionString = " ".join(VoteOptionString)
											VoteOptionString = VoteOptionString.replace("-","")
											VoteOptionString = VoteOptionString.split(" ")
											Count = 0
											global VoteListString
											while (Count < len(VoteOptionString)):
												yield from client.send_message(msg.channel, "{0}: `{1}`".format(Count+1,VoteOptionString[Count]))
												VoteListString.append(VoteOptionString[Count])
												Count += 1
											String = int(TimeString / 10)*10
											StringSecond = int(TimeString % 10)
											StringThird = int(String+StringSecond)
											
											game = discord.Game()
											game.name = "Time: "+str(StringThird)
											game.url = StringGame[1]
											game.type = 1
											yield from client.change_status(game=game)
											
											while (StringThird > String):
												yield from asyncio.sleep(1)
												StringThird -= 1
											else:
												while (String > 10):
													game = discord.Game()
													game.name = "Time: "+str(String)
													game.url = StringGame[1]
													game.type = 1
													yield from client.change_status(game=game)
													yield from asyncio.sleep(10)
													String -= 10
												else:
													while (StringSecond > 5):
														yield from asyncio.sleep(1)
														StringSecond -= 1
													else:
														while (StringSecond > 0):
															game = discord.Game()
															game.name = "Time: "+str(StringSecond)
															game.url = StringGame[1]
															game.type = 1
															yield from client.change_status(game=game)
															yield from asyncio.sleep(1)
															StringSecond -= 1
														else:
															yield from client.send_message(msg.channel, "Time's up")
															yield from asyncio.sleep(2)
															game = discord.Game()
															game.name = "Time: 0"
															game.url = StringGame[1]
															game.type = 1
															yield from client.change_status(game=game)
															VoteStart = 0
															VotedString = []
															global ListLengthCheck
															ListLengthCheck = 0
															if (len(VoteListString)-len(VoteOptionString)) >= 1:
																while (ListLengthCheck < len(VoteOptionString)):
																	IntVoteString = list(filter(lambda x: VoteOptionString[ListLengthCheck] in x, VoteListString))
																	ListLengthCheck += 1
																	if len(IntVoteString)-1 > 1:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nVoted: {2} times```".format(ListLengthCheck,VoteOptionString[ListLengthCheck-1],len(IntVoteString)-len(VoteOptionString)))
																	elif not IntVoteString:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nNot voted```".format(ListLengthCheck,VoteOptionString[ListLengthCheck-1]))
																	elif len(IntVoteString)-(len(VoteOptionString)-(len(VoteOptionString)-1)) == 1:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nVoted: {2} times```".format(ListLengthCheck,VoteOptionString[ListLengthCheck-1],"over 9000"))
																	else:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nVoted: {2} time```".format(ListLengthCheck,VoteOptionString[ListLengthCheck-1],len(IntVoteString)-1))
																else:
																	yield from asyncio.sleep(5)
																	game = discord.Game()
																	game.name = "display poll results"
																	yield from client.change_status(game=game)
																	yield from asyncio.sleep(15)
																	game.name = StringGame[0]
																	game.url = StringGame[1]
																	game.type = StringGame[2]
																	yield from client.change_status(game=game)
															else:
																yield from client.send_message(msg.channel, "No votes received")
																yield from asyncio.sleep(5)
																game = discord.Game()
																game.name = StringGame
																yield from client.change_status(game=game)

									else:
										if VoteStart == 0:
											print("No tags found")
											global VoteStart
											VoteStart = 1
											global VotedString
											VotedString = []
											global VoteString
											VoteString = []
											global VoteListString
											VoteListString = []
											global VoteType
											VoteType = 0
											yield from client.send_typing(msg.channel)
											yield from client.send_message(msg.channel, "Started poll:\n```{}```\nTo vote type `vote @<user>`".format(PollContentString))
											String = int(GameString / 10)*10
											StringSecond = int(GameString % 10)
											StringThird = int(String+StringSecond)
											
											game = discord.Game()
											game.name = "Time: "+str(StringThird)
											yield from client.change_status(game=game)
											
											while (StringThird > String):
												yield from asyncio.sleep(1)
												StringThird -= 1
											else:
												while (String > 10):
													game = discord.Game()
													game.name = "Time: "+str(String)
													yield from client.change_status(game=game)
													yield from asyncio.sleep(10)
													String -= 10
												else:
													while (StringSecond > 5):
														yield from asyncio.sleep(1)
														StringSecond -= 1
													else:
														while (StringSecond > 0):
															game = discord.Game()
															game.name = "Time: "+str(StringSecond)
															yield from client.change_status(game=game)
															yield from asyncio.sleep(1)
															StringSecond -= 1
														else:
															yield from client.send_message(msg.channel, "Time's up")
															game = discord.Game()
															game.name = "Time: 0"
															yield from client.change_status(game=game)
															VoteStart = 0
															VotedString = []
															global ListLengthCheck
															ListLengthCheck = 0
															if len(VoteListString) >= 1:
																while (ListLengthCheck < len(VoteString)):
																	MemberVoteString = list(filter(lambda x: str(VoteString[ListLengthCheck]) in x, VoteListString))
																	ListLengthCheck = ListLengthCheck + 1
																	if len(MemberVoteString) > 1:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nVoted: {2} times```".format(ListLengthCheck,msg.server.get_member(VoteString[ListLengthCheck-1]).name,len(MemberVoteString)))
																	elif len(VoteListString) == 1:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nVoted: {2} times```".format(ListLengthCheck,msg.server.get_member(VoteString[ListLengthCheck-1]).name,"over 9000"))
																	else:
																		yield from client.send_message(msg.channel, "```{0} - {1}\nVoted: {2} time```".format(ListLengthCheck,msg.server.get_member(VoteString[ListLengthCheck-1]).name,len(MemberVoteString)))
																else:
																	yield from asyncio.sleep(5)
																	game = discord.Game()
																	game.name = "display poll results"
																	yield from client.change_status(game=game)
																	yield from asyncio.sleep(15)
																	game.name = StringGame
																	yield from client.change_status(game=game)
															else:
																yield from client.send_message(msg.channel, "No votes received")
																yield from asyncio.sleep(5)
																game = discord.Game()
																game.name = StringGame
																yield from client.change_status(game=game)

						elif Message.startswith("vote"):
							if VoteStart == 1:
								Vote = msg.raw_mentions
								global VoteInt
								VoteInt = Message
								VoteInt = VoteInt.split(" ")
								del VoteInt[0]
								VoteInt = " ".join(VoteInt)
								if msg.author.id in VotedString:
									yield from client.send_message(msg.channel, "You already have voted once, try waiting till next poll before you vote again.")
								else:
									if VoteType == 0:
										if len(Vote) == 1:
											VotedString.append(msg.author.id)
											global VoteCheckString
											VoteCheckString = " ".join(Vote)
											global VoteListString
											if VoteCheckString in VoteString:
												yield from client.send_message(msg.channel, "Succesfully registered vote of {0} voting {1}".format(msg.author.name, msg.mentions[0].name))
												VoteListString.append(VoteCheckString)
											else:
												yield from client.send_message(msg.channel, "Succesfully registered vote of {0} voting {1}".format(msg.author.name, msg.mentions[0].name))
												VoteString.append(VoteCheckString)
												VoteListString.append(VoteCheckString)
										else:
											yield from client.send_message(msg.channel, "Too many IDs mentioned, use {} less".format(len(Vote-1)))
									else:
										if len(VoteInt) == 1:
											if int(VoteInt) <= len(VoteOptionString):
												if int(VoteInt) > 0:
													VotedString.append(msg.author.id)
													global VoteListString
													VoteInt = int(VoteInt)-1
													VoteListString.append(VoteOptionString[VoteInt])
													yield from client.send_message(msg.channel, "Succesfully registered vote of {0} voting `{1}`".format(msg.author.name, VoteOptionString[int(VoteInt)]))
												else:
													yield from client.send_message(msg.channel, "Don't vote on non-existing values")
											else:
												yield from client.send_message(msg.channel, "Don't vote on non-existing values")
										else:
											yield from client.send_message(msg.channel, "Too many votes registered, try using {} less".format(len(VoteInt-1)))
						
						elif Message.startswith("lmgtfy"):
							Message = Message.split(" ")
							del Message[0]
							Message = "+".join(Message)
							yield from client.send_message(msg.channel,"http://lmgtfy.com/?q={0}".format(Message))
						
						elif Message.startswith("google"):
							Message = Message.split(" ")
							del Message[0]
							Message = "+".join(Message)
							yield from client.send_message(msg.channel,"https://www.google.nl/#q={0}".format(Message))
						
						elif Message.startswith("steam"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							yield from client.send_message(msg.channel, "https://steamcommunity.com/linkfilter/?url={0}".format(Message))
						
						elif Message.startswith("hex2ascii"):
							Message = Message.split(" ")
							del Message[0]
							Message = " ".join(Message)
							AsciiString = bytes.fromhex(Message).decode('utf-8')
							yield from client.send_message(msg.channel, AsciiString)
							
						elif Message.startswith("how") and Message.endswith("is that"):
							Message = Message.split(" ")
							del Message[0]
							MessageLen = len(Message)
							del Message[MessageLen-1]
							del Message[MessageLen-2]
							Message = " ".join(Message)
							yield from client.send_message(msg.channel,"`Pretty {}`".format(Message))

		except IndexError:
			pass
	except:
		FailString = traceback.format_exc()
		print("Error: ", FailString)
		yield from client.send_message(client.get_channel("180793320145027072"),'Error:\n```Error: {0}\nServer: {1}\nChannel: {2}\nAuthor: {3}```'.format(FailString, msg.server.name, msg.channel.name, msg.author.name))
		yield from client.send_message(client.get_channel(LogChannel[0]), 'An exception has occured.\nThe exception contains the following message:\n`python\n{}`'.format(FailString))
		
print("Starting bot...")
#client.run(UserName, Password)
client.run(Password)

if not client.is_logged_in:
	print("Shutting down...")
	with open('./Settings/Gags.json', 'w') as GagFile:
		json.dump(GagList, GagFile)
		print("Saved {} gagged users".format(len(GagList)))
	with open('./Settings/LogChannel.json', 'w') as LogFile:
		json.dump(LogChannel, LogFile)
		print("Saved current logging Channel and Server")
	with open('./Settings/Channels.json', 'w') as ChannelFile:
		json.dump(Channels, ChannelFile)
		print("Saved {} permitted channels".format(len(Channels)))
	with open('./Settings/Game.json', 'w') as GameFile:
		json.dump(StringGame, GameFile)
		print("Saved '{}' as current game".format(StringGame[0]))
	with open('./Settings/Panel.json', 'w') as PanelFile:
		json.dump(PanelUser, PanelFile)
		print("Saved {} permitted users for music".format(len(PanelUser)))
	with open('./Settings/PlayList.json', 'w') as PlayListFile:
		json.dump(RadioList, PlayListFile)
		print("Saved {} songs to the playlist".format(len(RadioList)))
	with open('./Settings/Note.json', 'w') as NoteFile:
		json.dump(Note, NoteFile)
		print("Saved {} notes".format(len(Note)))
	with open('./Settings/Radio.json', 'w') as RadioFile:
		json.dump(VoiceChannelID, RadioFile)
		print("Saved the current radio channel")
	with open('./Settings/BannedSounds.json', 'w') as SoundFile:
		json.dump(BanSound, SoundFile)
		print("Saved {} banned sounds or directories".format(len(BanSound)))
	Database.close()
	time.sleep(10)
	exit
