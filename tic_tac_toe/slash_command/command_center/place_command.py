from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse

from slash_command.game_and_board.game import TTTGame
from django.http import JsonResponse

from slash_command.game_and_board.board import GameBoard

from slash_command.constants import MoveStatus

from slash_command.constants import GAME_STATUS_DRAW


class PlaceCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		if len(cmdParamsAsText) != 2:
			raise Exception("Bad usage")

		status, game = TTTGame.move(invokingChannelId, invokingUserId, int(cmdParamsAsText[0]), int(cmdParamsAsText[1]))
		if status == MoveStatus.NO_GAME:
			return HttpResponse("There is no active game in this channel. Start one by using the command`/ttt invite @user`. See `/ttt help` for more details")
		if status == MoveStatus.NOT_VALID_USER:
			return HttpResponse("You are not a participant in the game. Current game is between {p1} and {p2}".format(p1=game.player1.slackUser, p2=game.player2.slackUser))
		if status == MoveStatus.NOT_YOUR_TURN:
			return JsonResponse(
				{
					"response_type": "in_channel",
					"text": "Its not your turn. Its {p}'s turn.".format(
						p=game.nextTurn.slackUser
					)
				}
			)
		if status == MoveStatus.MOVE_OUT_OF_BOARD:
			return HttpResponse("Not a valid position. Your row should be between 1-{r} and your column should be between 1-{c}".format(r=game.nRows, c=game.nCols))
		if status == MoveStatus.NOT_EMPTY:
			return HttpResponse("Not a valid Slot. Slot is already occupied. Please use `/ttt show` to see where to move")
		if status == MoveStatus.MOVE_SUCCESS:
			return JsonResponse(
				{
					"response_type": "in_channel",
					"text": "Coin placement Success {p1}. Its your turn {p2}, place your coin wisely. Here is the board is {b}".format(
						p1=game.player1.slackUser if game.nextTurn == game.player2 else game.player2.slackUser,
						p2=game.nextTurn.slackUser,
						b=GameBoard.initFromGame(game).pretty()
					)
				}
			)
		if status == MoveStatus.GAME_ENDED:
			if game.status == GAME_STATUS_DRAW:
				return JsonResponse(
					{
						"response_type": "in_channel",
						"text": "Congrats to both of you {p1} and {p2}. Its a DRAW!!!. You have brilliantly matched one another. Here is the final board is {b}".format(
							p1=game.player1.slackUser,
							p2=game.player2.slackUser,
							b=GameBoard.initFromGame(game).pretty()
						)
					}
				)
			else:
				return JsonResponse(
					{
						"response_type": "in_channel",
						"text": "Congrats {p1}. You Won!. The game is won by {p1}. Better luck next time {p2}. Here is the final board is {b}".format(
							p1=game.wonBy.slackUser,
							p2=game.lostBy.slackUser,
							b=GameBoard.initFromGame(game).pretty()
						)
					}
				)





