from functools import wraps

from django.http import HttpResponseForbidden

def authenticate_slack(func):
	@wraps(func)
	def inner(*args, **kwargs):
		if args[0].POST.get('token') != 'hpjMTmHvY2OoWSuEH1rzbY3T':
			return HttpResponseForbidden()
		return func(*args, **kwargs)

	return inner