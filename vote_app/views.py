from django.shortcuts import render
from django.http import HttpResponse
from .models import Poll, Poll_Option
from django.contrib.auth.decorators import login_required



def index(request):
    ls = Poll.objects.all()  # Retrieve all objects from Poll model
    output = ', '.join([p.name for p in ls])  # Example of accessing attribute, adjust as per your model fields
    return HttpResponse("<h1>%s</h1>" % output)

def index_id(request,id):
    ls = Poll.objects.get(id = id) # Retrieve all objects from Poll model
    return HttpResponse("<h1>%s</h1>" % ls.name)

def main(response):
    return HttpResponse("<h1>Main</h1>")

@login_required
def dashboard(request):
    return HttpResponse("<h1>Dashboard</h1>")

@login_required
def about(request):
    return HttpResponse("<h1>About</h1>")