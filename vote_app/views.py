from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Poll, Poll_Option
from django.views.decorators.csrf import csrf_exempt



def homepage(request):
    return render(request, 'homepage.html', {})

def index(request):
    ls = Poll.objects.all()  # Retrieve all objects from Poll model
    output = ', '.join([p.name for p in ls])  # Example of accessing attribute, adjust as per your model fields
    return HttpResponse("<h1>%s</h1>" % output)

def index_id(request,id):
    ls = Poll.objects.get(id = id) # Retrieve all objects from Poll model
    return HttpResponse("<h1>%s</h1>" % ls.name)

def about(request):
    return render(request, 'about.html')

def account(request):
    return render(request, 'account.html')

def create_poll(request):
    return render(request, 'create_poll.html')

def manage_elections(request):
    return render(request, 'manage_elections.html')

def submit_poll(request):
    if request.method == 'POST':
        # Process form data (save poll, update database, etc.)
        # Example: Save poll data to the database
        question1 = request.POST.get('question1')
        option1_1 = request.POST.get('option1_1')

        # Redirect to homepage after successful submission
        return redirect('home')
    return redirect('create_poll')

def change_password(request):
    # Handle change password logic
    return render(request, 'change_password.html')

@csrf_exempt
def submit_password(request):
    # Handle POST request for changing password here
    if request.method == 'POST':
        # Process form data here
        # Redirect to homepage after processing
        return redirect('home')  # Replace 'home' with the name of your homepage URL pattern
    else:
        # Handle other HTTP methods as needed
        return redirect('home')  # Redirect to homepage for other methods
