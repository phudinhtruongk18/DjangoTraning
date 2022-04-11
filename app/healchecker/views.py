from django.http.response import HttpResponse
from .tasks import add

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.
def total(request):
    res = add.delay(4,5)
    return HttpResponse(res)
