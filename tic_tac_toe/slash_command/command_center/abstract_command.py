from abc import ABCMeta
from abc import abstractmethod

class AbstractSlashCommand(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def handle(self, invokingChannelId, invokingChannelName, invokingUserId, invokingUserName, command, cmdParamsAsText):
		pass
