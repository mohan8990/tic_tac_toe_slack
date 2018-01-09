from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse

from slash_command.models import Game
from django.http import JsonResponse

from slash_command.constants import GAME_STATUS_WON

from slash_command.constants import GAME_STATUS_DRAW

from slash_command.constants import GAME_STATUS_ABANDONED
from collections import defaultdict

class StatsCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		if cmdParamsAsText:
			raise Exception("Bad Params")

		games = Game.objects.filter(channel__channelId=invokingChannelId)
		if len(games) == 0:
			return JsonResponse(
				{
					"response_type": "in_channel",
					"text": "We are yet to play a game in this channel. Try `/ttt invite @user` to start a game. `/ttt help` for more details"
				}
			)

		numWins = games.filter(status=GAME_STATUS_WON).count()
		numDraw = games.filter(status=GAME_STATUS_DRAW).count()
		numCancelled = games.filter(status=GAME_STATUS_ABANDONED).count()
		mostWin = None
		mostWinCount = 0
		if numWins > 0:
			playerByWins = defaultdict(int)
			for game in games.filter(status=GAME_STATUS_WON):
				playerByWins[game.wonBy] += 1
			firstSorted = sorted(playerByWins.iteritems(), key=lambda (k,v): (v,k), reverse=True)[0]
			mostWin = firstSorted[0]
			mostWinCount = firstSorted[1]

		return JsonResponse(
			{
				"response_type": "in_channel",
				"text": "This channel has seen a total of {t} games. {w} won and {d} ended in a draw. {c} games were abandoned in between. {moreData}".format(
					t=len(games),
					w=numWins,
					d=numDraw,
					c=numCancelled,
					moreData="" if numWins == 0 else ("{p} won most games. {p}'s trophy count is {tc}".format(p=mostWin.slackUser, tc=mostWinCount))
				)
			}
		)

