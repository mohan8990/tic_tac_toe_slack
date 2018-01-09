from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse

from slash_command.game_and_board.game import TTTGame
from django.http import JsonResponse

from slash_command.game_and_board.board import GameBoard

from slash_command.constants import CancelStatus


class CancelCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		if cmdParamsAsText:
			raise Exception("Bad usage")

		cancelStatus, game = TTTGame.cancel(invokingChannelId, invokingUserId)
		if cancelStatus == CancelStatus.NO_GAME:
			return HttpResponse("There are no active games in this channel to cancel. Start one by using `/ttt invite @user`")
		if cancelStatus == CancelStatus.NOT_PARTICIPANT:
			return HttpResponse("Sorry, you are not the participant. Game is between {p1} and {p2}".format(p1=game.player1.slackUser, p2=game.player2.slackUser))
		if cancelStatus == CancelStatus.SUCCESS:
			return JsonResponse(
				{
					"response_type": "in_channel",
					"text": "The current game is between {p1} and {p2} is cancelled. Last config of board is {b}".format(
						p1=game.player1.slackUser,
						p2=game.player2.slackUser,
						b=GameBoard.initFromGame(game).pretty()
					)
				}
			)