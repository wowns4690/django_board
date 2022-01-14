import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from user.models import User


# Create your views here.


def hello(request):
    context = {}

    login_session = request.session.get('login_session', '')

    if login_session == '':
        context['login_session'] = False
    else:
        context['login_session'] = True

    return render(request, 'home/index.html', context)


@csrf_exempt
def ajax(request):
    if request.method == 'POST':
        data = {
            'msg': json.loads(request.body)
        }

    return JsonResponse(data)
