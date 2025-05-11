from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def gettext(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response = {
                'status': 'success',
                'summary': data['text'][:2000]
            }
        except json.JSONDecodeError:
            response = {
                'status': 'error',
                'summary': 'Invalid JSON data'
            }

        with open('data.txt', "w", encoding="utf-8") as f:
            f.write(data['text'])
        
    else:
        response = {
            'status': 'error',
            'summary': 'Only POST requests are allowed'
        }
        return HttpResponse("<a href='https://stackoverflow.com/legal/cookie-policy' >here</a>")
    return JsonResponse(response)
