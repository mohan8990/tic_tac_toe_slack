import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class CommandCenter(object):
	def __init__(self, postData):
		self.postData = postData
		for k, v in postData.iteritems():
			logger.info('{}: {}'.format(k, v)) # TODO: Restrict sensitive

	def response(self):
		return HttpResponse("Got it")
