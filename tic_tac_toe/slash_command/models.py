# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class GameUsers(models.Model):
	userName = models.TextField()
	# Slack user id
	userId = models.CharField(unique=True, max_length=100, db_index=True) # TODO: Check max length of user

	@property
	def winCount(self):
		pass

	@property
	def lossCount(self):
		pass

	@property
	def drawCount(self):
		pass

class GameChannels(models.Model):
	channelName = models.TextField()
	# slack channel id which comes in the request.
	channelId = models.CharField(unique=True, max_length=100, db_index=True) # Check max slack channel length

	@property
	def numGames(self):
		pass

	@property
	def numLoss(self):
		pass

	@property
	def numWin(self):
		pass

	@property
	def numDraw(self):
		pass


