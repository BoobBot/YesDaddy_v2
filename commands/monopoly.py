import discord
from typing import Union
import asyncio, os
import ast

from discord.ext import commands

from config.settings_config import monopoly_game_settings
from utils.monopoly_game import MonopolyGame
from views.monopoly_views import GetPlayersView


class Monopoly(commands.Cog):
	"""Play monopoly with 2-8 people."""
	def __init__(self, bot):
		self.bot = bot
		self.games = []
		self.config = monopoly_game_settings

	@commands.guild_only()
	@commands.group(invoke_without_command=True) 
	async def monopoly(self, ctx, savefile: str=None):
		"""
		Play monopoly with 2-8 people.
		
		Use the optional parameter "savefile" to load a saved game.
		"""
		if [game for game in self.games if game.channel == ctx.channel]:
			return await ctx.send('A game is already running in this channel.')
		channel = ctx.channel
		startCash = await self.config.get('startCash')
		if savefile is not None:
			guild_data = await self.bot.db_client.get_guild(ctx.guild.id)
			saves = guild_data.monopoly_saves
			if savefile not in saves:
				return await ctx.send(
					'There is no save file with that name.\n'
					'Does it need to be converted? '
					'Is it saved in another guild?\n'
					f'Use `{ctx.prefix}monopoly list` to list save files.'
				)
			data = saves[savefile]
			if ctx.author.id not in data['uid']:
				return await ctx.send('You are not a player in that game!')
			initial_message = await ctx.send(f'Using save file `{savefile}`')
			if (
				await self.config.get('useThreads')
				and ctx.channel.permissions_for(ctx.guild.me).create_public_threads
				and ctx.channel.type is discord.ChannelType.text
			):
				try:
					channel = await initial_message.create_thread(
						name='Monopoly',
						reason='Automated thread for Monopoly.',
					)
				except discord.HTTPException:
					pass
			game = MonopolyGame(ctx, channel, data=data)
			self.games.append(game)
		else:
			view = GetPlayersView(ctx, 8)
			initial_message = await ctx.send(view.generate_message(), view=view)
			if (
				await self.config.get('useThreads')
				and ctx.channel.permissions_for(ctx.guild.me).create_public_threads
				and ctx.channel.type is discord.ChannelType.text
			):
				try:
					channel = await initial_message.create_thread(
						name='Monopoly',
						reason='Automated thread for Monopoly.',
					)
				except discord.HTTPException:
					pass
			await view.wait()
			players = view.players
			if len(players) < 2:
				return await channel.send('Nobody else wants to play, shutting down.')
			uid = []
			for player in players[:8]:
				if isinstance(player, discord.Member):
					uid.append(player.id)
				else:
					uid.append(player)
			if [game for game in self.games if game.ctx.channel == ctx.channel]:
				return await channel.send('Another game started in this channel while setting up.')
			game = MonopolyGame(ctx, channel, startCash=startCash, uid=uid)
			self.games.append(game)
	
	@monopoly.command(name='list')
	async def monopoly_list(self, ctx):
		"""List available save files."""
		guild_data = await self.bot.db_client.get_guild(ctx.guild.id)
		saves = guild_data.monopoly_saves
		if not saves:
			return await ctx.send('There are no save files in this server.')
		savenames_in = '\n'.join(name for name in saves if ctx.author.id in saves[name]['uid'])
		savenames_out = '\n'.join(name for name in saves if ctx.author.id not in saves[name]['uid'])
		msg = ''
		if savenames_in:
			msg += f'\n[Saves you are in]\n{savenames_in}\n'
		if savenames_out:
			msg += f'\n[Saves you are not in]\n{savenames_out}\n'
		await ctx.send(f'```ini{msg}```')			
	
	# @checks.guildowner()
	# @monopoly.command()
	# async def delete(self, ctx, *savefiles: str):
	# 	"""
	# 	Delete one or more save files.
	#
	# 	This cannot be undone.
	# 	"""
	# 	if not savefiles:
	# 		return await ctx.send_help()
	# 	success = []
	# 	fail = []
	# 	async with self.config.guild(ctx.guild).saves() as saves:
	# 		for file in savefiles:
	# 			if file not in saves:
	# 				fail.append(file)
	# 				continue
	# 			del saves[file]
	# 			success.append(file)
	# 	msg = ''
	# 	if success:
	# 		msg += f'The following savefiles were deleted: `{humanize_list(success)}`\n'
	# 	if fail:
	# 		msg += f'The following savefiles were not found: `{humanize_list(fail)}`\n'
	# 	await ctx.send(msg)
	#
	# @commands.guild_only()
	# @commands.group(invoke_without_command=True, hidden=True)
	# async def monopolyconvert(self, ctx, savefile: str):
	# 	"""Convert a savefile to work with the latest version of this cog."""
	# 	if savefile in ('delete', 'list'):
	# 		return await ctx.send(
	# 			'You cannot convert a save file with that name as '
	# 			'it conflicts with the name of a new command.'
	# 		)
	# 	hold = []
	# 	for x in os.listdir(cog_data_path(self)):
	# 		if x[-4:] == '.txt':
	# 			hold.append(x[:-4])
	# 	if savefile in hold:
	# 		cfgdict = {}
	# 		with open(f'{cog_data_path(self)}/{savefile}.txt') as f:
	# 			for line in f:
	# 				line = line.strip()
	# 				if not line or line.startswith('#'):
	# 					continue
	# 				try:
	# 					key, value = line.split('=') #split to variable and value
	# 				except ValueError:
	# 					await ctx.send(f'Bad line in save file {savefile}:\n{line}')
	# 					continue
	# 				key, value = key.strip(), value.strip()
	# 				value = ast.literal_eval(value)
	# 				cfgdict[key] = value #put in dictionary
	# 		try:
	# 			uid = cfgdict['id']
	# 			del cfgdict['id']
	# 			cfgdict['uid'] = uid
	#
	# 			isalive = cfgdict['alive']
	# 			del cfgdict['alive']
	# 			cfgdict['isalive'] = isalive
	#
	# 			cfgdict['injail'] = cfgdict['injail'][1:]
	# 			cfgdict['tile'] = cfgdict['tile'][1:]
	# 			cfgdict['bal'] = cfgdict['bal'][1:]
	# 			cfgdict['goojf'] = cfgdict['goojf'][1:]
	# 			cfgdict['isalive'] = cfgdict['isalive'][1:]
	# 			cfgdict['jailturn'] = cfgdict['jailturn'][1:]
	# 			cfgdict['injail'] = cfgdict['injail'][1:]
	# 			cfgdict['uid'] = cfgdict['uid'][1:]
	# 			cfgdict['p'] -= 1
	# 			cfgdict['ownedby'] = [x - 1 for x in cfgdict['ownedby']]
	# 			cfgdict['freeparkingsum'] = 0
	# 		except Exception:
	# 			return await ctx.send('One or more values are missing from the config file.')
	# 		try:
	# 			del cfgdict['tilename']
	# 		except Exception:
	# 			pass
	# 		for key in (
	# 			'injail', 'tile', 'bal', 'ownedby', 'numhouse',
	# 			'ismortgaged', 'goojf', 'isalive', 'jailturn', 'p',
	# 			'num', 'numalive', 'uid', 'freeparkingsum'
	# 		):
	# 			if key not in cfgdict:
	# 				return await ctx.send(
	# 					f'The value "{key}" is missing from the config file.'
	# 				)
	# 		savefile = savefile.replace(' ', '')
	# 		async with self.config.guild(ctx.guild).saves() as saves:
	# 			if savefile in saves:
	# 				await ctx.send('There is already another save with that name. Override it?')
	# 				try:
	# 					response = await self.bot.wait_for(
	# 						'message',
	# 						timeout=60,
	# 						check=lambda m: (
	# 							m.channel == ctx.channel
	# 							and m.author == ctx.author
	# 						)
	# 					)
	# 				except asyncio.TimeoutError:
	# 					return await ctx.send('You took too long to respond.')
	# 				if response.content.lower() not in ('yes', 'y'):
	# 					return await ctx.send('Not overriding.')
	# 			saves[savefile] = cfgdict
	# 		await ctx.send('Savefile converted successfully.')
	# 	elif hold:
	# 		savenames = '\n'.join(hold)
	# 		return await ctx.send(
	# 			f'That file does not exist.\nConvertable save files:\n```\n{savenames}```'
	# 		)
	# 	else:
	# 		return await ctx.send('You do not have any save files to convert.')
	#
	# @monopolyconvert.command(name='list')
	# async def monopolyconvert_list(self, ctx):
	# 	"""List save files that can be converted."""
	# 	saves = []
	# 	for x in os.listdir(cog_data_path(self)):
	# 		if x[-4:] == '.txt':
	# 			saves.append(x[:-4])
	# 	if saves:
	# 		savenames = '\n'.join(saves)
	# 		await ctx.send(f'Convertable save files:\n```\n{savenames}```')
	# 	else:
	# 		await ctx.send('You do not have any save files to convert.')
	#
	# @commands.guild_only()
	# @checks.guildowner()
	# @commands.command()
	# async def monopolystop(self, ctx):
	# 	"""Stop the game of monopoly in this channel."""
	# 	wasGame = False
	# 	for game in [g for g in self.games if g.channel == ctx.channel]:
	# 		game._task.cancel()
	# 		wasGame = True
	# 	if wasGame: #prevents multiple messages if more than one game exists for some reason
	# 		await ctx.send('The game was stopped successfully.')
	# 	else:
	# 		await ctx.send('There is no ongoing game in this channel.')
	#

	def cog_unload(self):
		return [game._task.cancel() for game in self.games]


async def setup(bot):
	await bot.add_cog(Monopoly(bot))