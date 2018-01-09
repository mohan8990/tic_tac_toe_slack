from functools import wraps
from django.conf import settings
from django.http import HttpResponseForbidden


def authenticate_slack(func):
	@wraps(func)
	def inner(*args, **kwargs):
		if args[0].POST.get('token') != settings.SLACK_SECRET_TOKEN:
			return HttpResponseForbidden()
		return func(*args, **kwargs)

	return inner