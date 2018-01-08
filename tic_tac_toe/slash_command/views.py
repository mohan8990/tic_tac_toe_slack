# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
from slash_command.security import authenticate_slack

from slash_command.command_center.slash_commands import CommandCenter


@csrf_exempt
@authenticate_slack
def slash_incoming(request):
	return CommandCenter(request.POST).response()