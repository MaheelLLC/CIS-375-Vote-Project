from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Poll, Poll_Option
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user.email = email  # Save email
            user.save()  # Save user with email
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    return render(request, 'vote_app/signup.html', {'form': form})

@login_required
def index(request):
    ls = Poll.objects.all()  # Retrieve all objects from Poll model
    output = ', '.join([p.name for p in ls])  # Example of accessing attribute, adjust as per your model fields
    return HttpResponse("<h1>%s</h1>" % output)

@login_required
def index_id(request, id):
    ls = Poll.objects.get(id=id)  # Retrieve all objects from Poll model
    return HttpResponse("<h1>%s</h1>" % ls.name)

@login_required
def main(response):
    return HttpResponse("<h1>Main</h1>")

@login_required
def dashboard(request):
    return HttpResponse("<h1>Dashboard</h1>")

@login_required
def about(request):
    return HttpResponse("<h1>About</h1>")
