from enum import Enum

DEFAULT_NULL_CHAR = ' '
DEFAULT_PLAYER1_CHAR = 'X'
DEFAULT_PLAYER2_CHAR = '0'

GAME_STATUS_WON = 'R'
GAME_STATUS_DRAW = 'D'
GAME_STATUS_ABANDONED = 'C'
GAME_STATUS_ACTIVE = 'A'
GAME_STATUS = (
	(GAME_STATUS_WON, 'Won or Lost by someone'),
	(GAME_STATUS_DRAW, 'Draw'),
	(GAME_STATUS_ABANDONED, 'Abandoned/Cancelled'),
	(GAME_STATUS_ACTIVE, 'Active')
)

class MoveStatus(Enum):
	MOVE_SUCCESS = 1
	NOT_EMPTY = 0
	GAME_ENDED = 2
	NOT_VALID_USER = 3
	NO_GAME = 4
	NOT_YOUR_TURN = 5
	MOVE_OUT_OF_BOARD=6

class CancelStatus(Enum):
	NO_GAME = 1
	NOT_PARTICIPANT = 2
	SUCCESS = 3
