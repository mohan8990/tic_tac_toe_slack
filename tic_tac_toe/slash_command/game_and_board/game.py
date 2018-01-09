from slash_command.game_and_board.board import GameBoard
from slash_command.constants import MoveStatus
from slash_command.constants import GAME_STATUS_ABANDONED
from slash_command.constants import GAME_STATUS_ACTIVE
from slash_command.models import Game
from slash_command.models import GameChannel
from slash_command.models import GameUser
from slash_command.constants import CancelStatus

from slash_command.constants import GAME_STATUS_DRAW
from slash_command.constants import GAME_STATUS_WON


class TTTGame(object):

	@classmethod
	def getActiveGame(cls, channelId):
		"""
		Will return the active game being played. Will return None if there are no active game.
		:param channelId: Slack Channel Id
		:return: Game object if there are any active games.
		"""
		game = cls.getLastGame(channelId)
		if game and game.status == GAME_STATUS_ACTIVE:
			return game
		return None

	@classmethod
	def getLastGame(cls, channelId):
		"""
		Show the last played Game in the channel or None if no game was played at all.
		:param channelId: A Valid slack channel Id
		"""
		return Game.objects.filter(channel__channelId=channelId).last()

	@classmethod
	def newGame(cls, channelId, channelName, player1Id, player1Name, player2Id, player2Name, nRows=3, nCols=3, numConsecutiveCoinsToWin=3):
		"""
		This will return None if it can't instantiate a new Game because of an active game. Otherwise, this will initialize
		an empty Board and will return the models.Game object

		:param channelId: slack channel id
		:param channelName: slack channel name (for bookkeping only)
		:param player1Id:  slack player 1 id
		:param player1Name: slack player 1 name (for bookkeeping only)
		:param nRows: Number of rows for the board
		:param nCols: Number of columns for the board
		:param numConsecutiveCoinsToWin: Number of consequtive coins one has to place to win.
		:return:
		"""
		if cls.getActiveGame(channelId): # Active game being played on.
			return None

		player1 = cls._getOrCreatePlayer(player1Id, player1Name)
		player2 = cls._getOrCreatePlayer(player2Id, player2Name)
		channel = cls._getOrCreateChannel(channelId, channelName)

		game = Game.objects.create(
			player1 = player1,
			player2 = player2,
			channel = channel,
			nRows = nRows,
			nCols = nCols,
			numConsecutiveCoinsToWin = numConsecutiveCoinsToWin
		)
		gameBoard = GameBoard.initDefault(game)
		gameBoard.saveBoard(game)
		return game

	@classmethod
	def move(cls, channelId, playerId, rowNum, colNum):
		"""
		Will place the playerId's coin to 1-based rowNum and and 1-based colNum.

		:param channelId: Slack API channelId
		:param playerId: Slack API playerId
		:param rowNum: 1-based rownum
		:param colNum: 1-index based colnum
		:return: Return value of the move and the game corresponding to the channelId.
		"""
		game = Game.objects.filter(channel__channelId=channelId).last()

		if not game or game.status != GAME_STATUS_ACTIVE:
			return MoveStatus.NO_GAME, game
		if playerId not in (game.player1.userId, game.player2.userId,):
			return MoveStatus.NOT_VALID_USER, game
		gameBoard = GameBoard.initFromGame(game)
		moveReturnVal = gameBoard.nextMove(game, playerId==game.player1.userId,row=rowNum,col=colNum)

		if moveReturnVal == MoveStatus.GAME_ENDED:
			if gameBoard.wonByPlayer1 or gameBoard.wonByPlayer2:
				game.status = GAME_STATUS_WON
				game.wonBy = game.player1 if gameBoard.wonByPlayer1 else game.player2
				game.lostBy = game.player1 if game.wonBy == game.player2 else game.player2
				game.save()
			else:
				game.status = GAME_STATUS_DRAW
				game.save()

		return moveReturnVal, game


	@classmethod
	def cancel(cls, channelId, invokingUserId):
		game = cls.getActiveGame(channelId)
		if not game:
			return CancelStatus.NO_GAME, None
		if invokingUserId not in (game.player1.userId, game.player2.userId):
			return CancelStatus.NOT_PARTICIPANT, game
		game.status = GAME_STATUS_ABANDONED
		game.save()
		return CancelStatus.SUCCESS, game


	@classmethod
	def _getOrCreatePlayer(cls, playerId, name):
		player, _ = GameUser.objects.get_or_create(userId=playerId)
		# User could have changed name.
		player.userName = name
		player.save()
		return player

	@classmethod
	def _getOrCreateChannel(cls, channelId, name):
		channel, _ = GameChannel.objects.get_or_create(channelId=channelId)
		# User could have changed name.
		channel.channelName = name
		channel.save()
		return channel
