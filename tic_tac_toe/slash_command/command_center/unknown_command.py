from slash_command.command_center.abstract_command import AbstractSlashCommand
from django.http import HttpResponse

class UnknownCommandHandler(AbstractSlashCommand):
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		return HttpResponse("Oops, Unknown command: `{}`".format(command))
