from django.http import HttpResponse,HttpResponseRedirect

def hello(request):
    return HttpResponse('hello python!')