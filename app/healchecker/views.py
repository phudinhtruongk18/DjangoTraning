from django.http.response import HttpResponse, JsonResponse
from .tasks import add

def total(request):
    res = add.delay(4,5)
    return HttpResponse(res)