from django.http import JsonResponse


def ping(request):
    data = {"ping": "pongg"}
    return JsonResponse(data)
