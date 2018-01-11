# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
from slash_command.constants import GAME_STATUS_ACTIVE
from slash_command.constants import GAME_STATUS
from slash_command.constants import DEFAULT_PLAYER1_CHAR
from slash_command.constants import DEFAULT_PLAYER2_CHAR
from slash_command.constants import DEFAULT_NULL_CHAR

from slash_command.constants import GAME_STATUS_WON

from slash_command.constants import GAME_STATUS_ABANDONED

from slash_command.constants import GAME_STATUS_DRAW


class GameUser(models.Model):
	userName = models.TextField()
	# Slack user id
	userId = models.CharField(unique=True, max_length=100, db_index=True) # TODO: Check max length of user

	@property
	def winCount(self):
		return self.wins.count()

	@property
	def lossCount(self):
		return self.losses.count()

	@property
	def slackUser(self):
		return "<@{}|{}>".format(self.userId, self.userName)

class GameChannel(models.Model):
	channelName = models.TextField()
	# slack channel id which comes in the request.
	channelId = models.CharField(unique=True, max_length=100, db_index=True) # Check max slack channel length

	@property
	def numGames(self):
		return self.games.count()

	@property
	def numWinOrLoss(self):
		return self.games.filter(status=GAME_STATUS_WON).count()

	@property
	def numAbandoned(self):
		return self.games.filter(status=GAME_STATUS_ABANDONED).count()

	@property
	def numDraw(self):
		return self.games.filter(status=GAME_STATUS_DRAW).count()

class Game(models.Model):
	status = models.CharField(max_length=1, db_index=True, choices=GAME_STATUS, default=GAME_STATUS_ACTIVE)
	player1 = models.ForeignKey(GameUser, related_name='+')
	player2 = models.ForeignKey(GameUser, related_name='+')
	player1Char = models.CharField(max_length=1, default=DEFAULT_PLAYER1_CHAR)
	player2Char = models.CharField(max_length=1, default=DEFAULT_PLAYER2_CHAR)
	nullChar = models.CharField(max_length=1, default=DEFAULT_NULL_CHAR)
	channel = models.ForeignKey(GameChannel, related_name='games')
	nRows = models.IntegerField()
	nCols = models.IntegerField()
	numConsecutiveCoinsToWin = models.IntegerField()
	wonBy = models.ForeignKey(GameUser, related_name='wins', null=True)
	lostBy = models.ForeignKey(GameUser, related_name='losses', null=True)

	@property
	def nextTurn(self):
		return self.player1 if self.boards.last().currentTurn == self.player2 else self.player2


class Board(models.Model):
	"""
	Immutable board, used to store all the moves. We can retrace by calculating diff between current and old move.
	"""
	serializedBoard = models.TextField()
	createAt = models.DateTimeField(auto_now_add=True)
	game = models.ForeignKey(Game, related_name='boards')
	currentTurn = models.ForeignKey(GameUser, related_name='+')

