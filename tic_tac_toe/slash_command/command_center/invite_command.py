import logging

from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse
from django.http import JsonResponse

from slash_command.game_and_board.game import TTTGame

from slash_command.game_and_board.board import GameBoard

logger = logging.getLogger(__name__)

class InviteCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		logger.info("In the invite command handler with command {} params {}. Invoking channel id {} invoking channel name {} invoking user id {} invoking user name {}".format(command, cmdParamsAsText, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName))

		if len(cmdParamsAsText) > 4 or len(cmdParamsAsText) < 1:
			raise Exception("Bad usage")

		invitingUser = cmdParamsAsText[0]
		numRows = numCols = numConsecutiveMoveToWin = 3
		if len(cmdParamsAsText) > 1:
			numRows = int(cmdParamsAsText[1])
			numCols = int(cmdParamsAsText[2])
		if len(cmdParamsAsText) == 4:
			numConsecutiveMoveToWin = int(cmdParamsAsText[3])

		logger.info("Inviting User {} numRows {} numCols {} numConsequtiveMoveToWin {}".format(invitingUser, numRows, numCols, numConsecutiveMoveToWin))
		if numConsecutiveMoveToWin > max(numRows,numCols):
			return HttpResponse("ERROR: Sorry, cannot create a game with numConsecutiveCoinsToWin as {} while numRows is {} and numCols is {}. numConsecutiveCoinsToWin should be less than or equal to {}".format(numConsecutiveMoveToWin, numRows, numCols, max(numRows, numCols)))

		invitingUserId, invitingUserName = invitingUser.split("|")
		invitingUserId = invitingUserId[2:]
		invitingUserName = invitingUserName[:-1]
		invokingUser = "<@{}|{}>".format(invokingUserId, invokingUserName)
		logger.info("Inviting user id: {} Inviting User name: {} Invoking User Id: {} Invoking User name: {}".format(invitingUserId, invitingUserName, invokingUserId, invokingUserName))

		if invitingUserId == invokingUserId:
			return HttpResponse("Sorry {} you cannot play game with yourself. Invite some other user".format(invokingUserName))

		activeGame = TTTGame.getActiveGame(invokingChannelId)
		if activeGame:
			return HttpResponse("Sorry. There is an ongoing game in this channel between {} and {}. Use `/ttt show` for more details".format(activeGame.player1.slackUser, activeGame.player2.slackUser))

		game = TTTGame.newGame(invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, invitingUserId, invitingUserName, numRows, numCols, numConsecutiveMoveToWin)
		gameBoard = GameBoard.initFromGame(game)
		boardAsText = gameBoard.pretty()
		return JsonResponse(
			{
				"response_type": "in_channel",
				"text": "Game Started between {p1} and {p2}. You have to place {n} consequtive pieces to win this game. Its {p1}'s turn. Current Board is {b}".format(p1=invokingUser, p2=invitingUser, n=numConsecutiveMoveToWin, b=boardAsText),
			}
		)
