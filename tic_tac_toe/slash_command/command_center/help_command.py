from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse

class HelpCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		if cmdParamsAsText:
			return HttpResponse('Usage: `/ttt help`. Additional Params `{}` not needed'.format(" ".join(cmdParamsAsText)))
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
				6) `/ttt invite @user 4 6`
					Will invite @user to play and will start with a board of 4x6.
				6) `/ttt invite @user 4 6 3`
					Will invite @user to play and will start with a board of 4x6. 3 consecutive coins of a player wins the game.
				7) `/ttt cancel`
					Will cancel any current game. Only active participants can cancel the game.
			'''
		return HttpResponse(ret)
