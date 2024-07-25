from django.http import HttpResponse
from .models import Poll, Poll_Option
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'vote_app/change_password.html'
    success_url = reverse_lazy('account')  # Redirect to the account page after a successful password change

@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, user=request.user)
    if request.method == 'POST':
        poll.delete()
        return redirect('election_page')
    return render(request, 'vote_app/delete_poll_confirm.html', {'poll': poll})


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


@csrf_exempt  # Only for demonstration; use proper CSRF protection in production
@login_required
def submit_poll(request):
    if request.method == 'POST':
        questions = []
        options = {}

        # Extract questions and options from POST data
        for key, value in request.POST.items():
            if key.startswith('question'):
                question_number = key.replace('question', '')
                questions.append(value)
                options[question_number] = []
            elif key.startswith('option'):
                question_number, option_number = key.replace('option', '').split('_')
                options[question_number].append(value)

        # Create Poll instances for each question and their options
        user = request.user
        for question_number, question in enumerate(questions, start=1):
            poll = Poll.objects.create(name=question, user=user)
            for option in options[str(question_number)]:
                Poll_Option.objects.create(poll=poll, text=option, votes=0)

        return redirect('home')
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
