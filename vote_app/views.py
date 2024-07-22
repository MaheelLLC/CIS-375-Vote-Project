from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Poll, Poll_Option
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt

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
    return render(request, 'vote_app/login_page.html', {'form': form})

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
            # Debugging: print form errors
            print("Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'vote_app/register_page.html', {'form': form})

@login_required
# def index(request):
#     ls = Poll.objects.all()  # Retrieve all objects from Poll model
#     output = ', '.join([p.name for p in ls])  # Example of accessing attribute, adjust as per your model fields
#     return HttpResponse("<h1>%s</h1>" % output)

def index(request):
    polls = Poll.objects.all()  # Retrieve all polls from the database
    return render(request, 'home_page.html', {'polls': polls})
    

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
def home_page(request):
    polls = Poll.objects.all()  # Fetch all Poll objects from the database
    return render(request, 'home_page.html' , {'polls': polls})

@login_required
def account(request):
    return render(request, 'account.html')

@login_required
def election_page(request):
    polls = Poll.objects.all()  # Fetch all Poll objects from the database
    return render(request, 'election_page.html' , {'polls': polls})

@login_required
def create_poll(request):
    return render(request, 'create_poll.html')

@login_required
def manage_elections(request):
    return render(request, 'manage_elections.html')

# @csrf_exempt
# @login_required
# def submit_poll(request):
#     # POST requests occur when submitting a form
#     if request.method == 'POST':
#         # Process form data (save poll, update database, etc.)
#         # Example: Save poll data to the database
#         question1 = request.POST.get('question1')
#         option1_1 = request.POST.get('option1_1')

#         # Redirect to homepage after successful submission
#         return redirect('home')
#     return redirect('create_poll')

@csrf_exempt  # Only for demonstration; use proper CSRF protection in production
@login_required
def submit_poll(request):
    if request.method == 'POST':
        question = request.POST.get('question1')
        # options = request.POST.getlist("options")
        option1 = request.POST.get('option1_1')
        option2 = request.POST.get('option1_2')

        # Create a new Poll instance
        user = request.user
        poll = Poll.objects.create(name=question, user = user)
        

        # Create PollOption instances associated with the poll
        Poll_Option.objects.create(poll=poll, text=option1, votes=0)
        Poll_Option.objects.create(poll=poll, text=option2, votes=0)
        all_polls = Poll.objects.all()
        # Print each poll's name
        for poll in all_polls:
            print(f"Poll ID: {poll.id}, Name: {poll.name}")


        return redirect('home')  # Redirect to home page or wherever appropriate
    else:
        return redirect('create_poll')  # Redirect back to create poll page if not a POST request


@csrf_exempt  
@login_required
def delete_all_polls(request):
    Poll.objects.all().delete()
    return redirect('home') 

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

def vote(request, slug):
    polls = Poll.objects.filter(slug=slug)
    
    if not polls.exists():
        # Handle the case where no poll exists
        return HttpResponse("No poll found", status=404)
    
    poll = polls.first()  # Get the first poll if multiple are found
    options = Poll_Option.objects.filter(poll=poll)
    
    msg = None
    
    if poll.voters.filter(id=request.user.id).exists():
        msg = 'voted'
        
    if request.method == 'POST':
        # selected option is the option id sent from template
        selected_option = request.POST.get("option")
        # option is the object that has that id
        option = Poll_Option.objects.get(id=selected_option)
        
        option.votes += 1
        # add user to list of people who already voted
        poll.voters.add(request.user)
        
        option.save()
        poll.save()
        # redirect to results when it exists
        return redirect('home')
        
    context = {"poll": poll, "options": options, "msg": msg}
    
    return render(request, "vote.html", context)
