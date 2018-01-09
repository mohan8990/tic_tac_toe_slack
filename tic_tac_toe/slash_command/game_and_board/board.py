import json

from slash_command.models import Board
from slash_command.constants import MoveStatus
from slash_command.constants import DEFAULT_NULL_CHAR

from slash_command.constants import GAME_STATUS_WON

from slash_command.constants import GAME_STATUS_DRAW


class GameBoard(object):

	def __init__(self, arr, player1Char, player2Char, isPlayer1CurrentTurn, numConsecutiveCoinsToWin, nullChar=DEFAULT_NULL_CHAR, game=None):
		self.arr = arr
		self.player1Char = player1Char
		self.player2Char = player2Char
		self.isPlayer1CurrentTurn = isPlayer1CurrentTurn
		self.nullChar = nullChar
		self.numConsecutiveCoinsToWin = numConsecutiveCoinsToWin
		self.wonByPlayer1 = False
		self.wonByPlayer2 = False
		self.isGameEnded = self._checkAndSetIfEnded()
		self.game = game


	def nextMove(self, game, isPlayer1, row, col):
		"""
		Will move player1/player2's coin to a 1 based index row and col.
		This will save the new board config if the move is a success.
		For a valid player1 next move, self.isPlayer1CurrentTurn should be false (i.e,
		GameBoard with currentTurn as player 1 will have player2 as next move user, etc).

		:param isPlayer1: differentiate player1 and player 2.
		:param game: models.Game object
		:param row: 1 index based row
		:param col: 1 index based col
		:return: Will return a Enum response indicating the status of the move.
		"""
		playerChar = self.player1Char if isPlayer1 else self.player2Char

		if self.isPlayer1CurrentTurn and isPlayer1:
			return MoveStatus.NOT_YOUR_TURN
		if not self.isPlayer1CurrentTurn and not isPlayer1:
			return MoveStatus.NOT_YOUR_TURN

		row -= 1
		col -= 1

		if row >= len(self.arr) or col >= len(self.arr[0]) or row < 0 or col < 0:
			return MoveStatus.MOVE_OUT_OF_BOARD

		if self.arr[row][col] != self.nullChar:
			return MoveStatus.NOT_EMPTY

		self.arr[row][col] = playerChar
		self.isPlayer1CurrentTurn = isPlayer1
		self.saveBoard(game)
		if self._checkAndSetIfEnded():

			return MoveStatus.GAME_ENDED


		return MoveStatus.MOVE_SUCCESS

	def whoWon(self):
		"""
		If anyone has won, it will return the 1 based player index. 1 if player 1 has won 2 if 2 has won.
		0 will be returned if Game is not won by anyone and resulted in a draw. -1 will be returned if its still active.
		:return: 0 - Draw. 1 - Won by player1, 2- won by player 2. -1 - Still ongoing.
		"""
		if self.isGameEnded:
			return 1 if self.wonByPlayer1 else 2
		return 0

	def pretty(self):
		"""
		Will return a pretty config of the current board which could be directly consumed either as text or as attachment
		"""
		arr=self.arr
		toRet = []
		str = "|"
		for j in range(len(arr[0]) - 1):
			str += "---+"
		str += "---|"
		toRet.append(str)
		for i in range(len(arr)):
			str = "| "
			str += " | ".join(arr[i])
			str += " |"
			toRet.append(str)
			str = "|"
			for j in range(len(arr[i]) - 1):
				str += "---+"
			str += "---|"
			toRet.append(str)
		return "\n\n{p1}'s coin: `{p1c}`\n{p2}'s coin: `{p2c}` ```{b}```".format(p1=self.game.player1.slackUser, p2=self.game.player2.slackUser, p1c=self.player1Char, p2c=self.player2Char, b="\n".join(toRet))

	def serializeBoardConfig(self):
		"""
		:param board: Game Board object
		:return: Serialized Text.
		"""
		return json.dumps(self.arr)


	def _checkAndSetIfEnded(self):

		def getCharAt(i, j):
			if i < 0 or i >= len(self.arr):
				return 'B' # Some dummy. Shouldn't use null char.
			if j < 0 or j >= len(self.arr[0]):
				return 'B'
			return self.arr[i][j]

		def getCharOfPlayerWon():
			rowCache = [[1 for i in range(len(self.arr[0]))] for j in range(len(self.arr))]
			colCache = [[1 for i in range(len(self.arr[0]))] for j in range(len(self.arr))]
			rDiagCache = [[1 for i in range(len(self.arr[0]))] for j in range(len(self.arr))]
			lDiagCache = [[1 for i in range(len(self.arr[0]))] for j in range(len(self.arr))]

			for i in range(len(self.arr)):
				for j in range(len(self.arr[0])):

					if self.arr[i][j] == DEFAULT_NULL_CHAR:
						continue
					# Row
					if getCharAt(i, j-1) == self.arr[i][j]:
						rowCache[i][j] += rowCache[i][j-1]
						if rowCache[i][j] == self.numConsecutiveCoinsToWin:
							return self.arr[i][j]
					# Col
					if getCharAt(i-1, j) == self.arr[i][j]:
						colCache[i][j] += colCache[i-1][j]
						if colCache[i][j] == self.numConsecutiveCoinsToWin:
							return self.arr[i][j]
					# RDiag
					if getCharAt(i-1, j-1) == self.arr[i][j]:
						rDiagCache[i][j] += rDiagCache[i-1][j-1]
						if rDiagCache[i][j] == self.numConsecutiveCoinsToWin:
							return self.arr[i][j]
					#LDiag
					if getCharAt(i-1, j+1) == self.arr[i][j]:
						lDiagCache[i][j] += lDiagCache[i-1][j+1]
						if lDiagCache[i][j] == self.numConsecutiveCoinsToWin:
							return self.arr[i][j]
			return None
		winningPlayerChar = getCharOfPlayerWon()
		# Won by either of the player
		if winningPlayerChar:
			self.wonByPlayer1 = True if winningPlayerChar == self.player1Char else False
			self.wonByPlayer2 = True if winningPlayerChar == self.player2Char else False
			return True
		# Atleast one empty slot
		for i in range(len(self.arr)):
			for j in range(len(self.arr[0])):
				if self.arr[i][j] == DEFAULT_NULL_CHAR:
					return False
		# Game is a draw
		return True

	def saveBoard(self, game):
		"""
		Given the Game model and GameBoard instance, this will create a mutable instance of models.Board.
		Only invoke this method if you want to save instane of

		:param game: models.Board instance
		:param gameBoard: GameBoard instance.
		:return: The newly created models.Board instance.
		"""
		board = Board.objects.create(
			game=game,
			serializedBoard=self.serializeBoardConfig(),
			currentTurn=game.player1 if self.isPlayer1CurrentTurn else game.player2
		)
		return board


	@classmethod
	def deserializeBoardConfig(cls, boardConfigAsTextField):
		return json.loads(boardConfigAsTextField)


	@classmethod
	def initFromGame(cls, game):
		"""
		Init GameBoard object from the last known board config of the game model.
		:param game: models.Game model instance.
		:return: GameBoard instance.
		"""
		board = game.boards.last()
		return cls(cls.deserializeBoardConfig(board.serializedBoard), game.player1Char, game.player2Char, board.currentTurn == game.player1, game.numConsecutiveCoinsToWin, game.nullChar, game=game)


	@classmethod
	def initDefault(cls, game):
		"""
		Initialize a default GameBoard Instance for the given models.Game instance.
		This will throw an exception if the game already has some board.
		User should init default board and then should save board in-order to start a new game.

		:param game: models.Game instance
		:return: Return GameBoard instance.
		"""
		if game.boards.exists():
			raise Exception("Cannot initialize, Game already has board")

		arr = [[game.nullChar for i in range(game.nCols)] for j in range(game.nRows)]

		return cls(arr, game.player1Char, game.player2Char, False, game.numConsecutiveCoinsToWin, game.nullChar, game=game)

