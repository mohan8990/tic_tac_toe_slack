from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse

from slash_command.game_and_board.game import TTTGame
from django.http import JsonResponse

from slash_command.game_and_board.board import GameBoard


class ShowCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		if cmdParamsAsText:
			raise Exception("Bad usage")

		game = TTTGame.getActiveGame(invokingChannelId)
		if not game:
			return JsonResponse(
				{
					"response_type": "in_channel",
					"text": "There is no ongoing game in this channel."
				}
			)

		return JsonResponse(
			{
				"response_type": "in_channel",
				"text": "The current game is between {p1} and {p2}. Its {p}'s turn. Current Board is {b}".format(
					p1=game.player1.slackUser,
					p2=game.player2.slackUser,
					p=game.nextTurn.slackUser,
					b=GameBoard.initFromGame(game).pretty()
				)
			}
		)

