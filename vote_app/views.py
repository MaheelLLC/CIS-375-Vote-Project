from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Poll, Poll_Option
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'vote_app/loginPage.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'vote_app/registerPage.html', {'form': form})

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
    return render(request, 'vote_app/about.html')

@login_required
def homepage(request):
    return render(request, 'homepage.html', {})

@login_required
def account(request):
    return render(request, 'account.html')

@login_required
def create_poll(request):
    return render(request, 'create_poll.html')

@login_required
def manage_elections(request):
    return render(request, 'manage_elections.html')

@csrf_exempt
@login_required
def submit_poll(request):
    # POST requests occur when submitting a form
    if request.method == 'POST':
        # Process form data (save poll, update database, etc.)
        # Example: Save poll data to the database
        question1 = request.POST.get('question1')
        option1_1 = request.POST.get('option1_1')

        # Redirect to homepage after successful submission
        return redirect('home')
    return redirect('create_poll')

@login_required
def change_password(request):
    # Handle change password logic
    return render(request, 'change_password.html')

@csrf_exempt
@login_required
def submit_password(request):
    # POST requests occur when submitting a form
    if request.method == 'POST':
        # Process form data here
        # Redirect to homepage after processing
        return redirect('home')
    else:
        # Handle other HTTP methods as needed
        return redirect('home')  # Redirect to homepage for other methods
