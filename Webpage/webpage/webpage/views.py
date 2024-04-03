from django.http import HttpResponse
from django.template import loader
def landing(request):
    template = loader.get_template('landingpage.html')
    return HttpResponse(template.render())
def options(request):
    template = loader.get_template('options.html')
    return HttpResponse(template.render())
def rlogin(request):
    template = loader.get_template('researchers-login.html')
    return HttpResponse(template.render())
def llogin(request):
    template = loader.get_template('labelers-login.html')
    return HttpResponse(template.render())
def ldashboard(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render())
def rdashboard(request):
    template = loader.get_template('researchers dashboard.html')
    return HttpResponse(template.render())