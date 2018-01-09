import logging
from django.http import HttpResponse

from slash_command.command_center.help_command import HelpCommandHandler

from slash_command.command_center.unknown_command import UnknownCommandHandler

from slash_command.command_center.invite_command import InviteCommandHandler
from slash_command.command_center.show_command import ShowCommandHandler

import traceback

from slash_command.command_center.cancel_command import CancelCommandHandler

from slash_command.command_center.place_command import PlaceCommandHandler

from slash_command.command_center.stats_command import StatsCommandHandler

logger = logging.getLogger(__name__)

class CommandCenter(object):
	COMMAND_TO_HANDLER = {
		'help': HelpCommandHandler,
		'invite': InviteCommandHandler,
		'show': ShowCommandHandler,
		'cancel': CancelCommandHandler,
		'place': PlaceCommandHandler,
		'stats': StatsCommandHandler
	}

	def __init__(self, postData):
		self.postData = postData
		for k, v in postData.iteritems():
			logger.info('{}: {}'.format(k, v)) # TODO: Restrict sensitive


	def response(self):
		commandTxt = self.postData.get('text')
		invokingChannelId = self.postData.get('channel_id')
		invokingChannelName = self.postData.get('channel_name')
		invokingUserId = self.postData.get('user_id')
		invokingUserName =  self.postData.get('user_name')
		logger.info("Command text is {} invoking channel id {} invoking channel name {} invoking user id {} invoking channel name ".format(commandTxt, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName))
		splitCommandTxt = commandTxt.split(" ")
		command = splitCommandTxt[0]
		commandParams = splitCommandTxt[1:]
		try:
			cls = self.COMMAND_TO_HANDLER.get(command, UnknownCommandHandler)
			logger.info("Invoking handler {} for commandText {} and params {}".format(cls, command, commandParams))
			return cls().handle(invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, commandParams)
		except Exception as e:
			logger.error("Encounterd error when processing commandText {} and Execption is {}.".format(commandTxt, e,))
			traceback.print_exc()
			return HttpResponse("Bad usage `{}`. Please refer `/ttt help` for more details.".format(commandTxt))


	def processHelpCommandAndResponse(self):
		ret = '''
		
			Usage: `/ttt <command> <arguments_if_any>`
			1) `/ttt stats` 
				Will show statistics of all the games in current channel
			2) `/ttt show`
				Show the current board config, its players and next turn. 
			3) `/ttt invite @user`
				Will invite the @user to play the game. Will fail if there is already an active game
			4) `/ttt place row, col`
				Will place your coin in row and col. Will succeed only when its your turn.
			5) `/ttt last`
				Show the last game which was played
			6) `/ttt invite @user 4 6`
				Will invite @user to play and will start with a board of 4x6.
			6) `/ttt invite @user 4 6 3`
				Will invite @user to play and will start with a board of 4x6. 3 consecutive coins of a player wins the game.
		'''
		return HttpResponse(ret)