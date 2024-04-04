from django.http import HttpResponse
from django.template import loader
import django.shortcuts as s
import json
def landing(request):
    return s.render(request, 'landingpage.html')
def options(request):
    return s.render(request, 'options.html')
def rlogin(request):
    return s.render(request, 'researchers-login.html')
def llogin(request):
    return s.render(request, 'labelers-login.html')
def ldashboard(request):
    print(request.POST.get('labeler-id'))
    return s.render(request, 'labelers dashboard.html')
def rdashboard(request):
    return s.render(request, 'researchers dashboard.html')
def rdata(request):
    return s.render(request, 'researchers data.html')