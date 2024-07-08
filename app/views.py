from django.shortcuts import render
# Django comes with a built-in User Creation Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Poll, Option

# Create your views here.
def index(request):
    # we'll just include all of the polls in the homepage
    polls = Poll.objects.all()
    context = {"polls": polls}
    return render(request, "index.html", context)

def signup(request):
    # since this is going as context in the webpage, we need it to appear as an 
    # empty form (I think we could actually move this line down)
    # UserCreationForm does two things: it creates a User object and it 
    # creates html input elements
    form = UserCreationForm()
    # the user is signing up for an account
    if request.method == 'POST':
        # fill in the form content with the user's input
        form = UserCreationForm(request.POST)
        # if the user's input fills in all fields and matches expected data 
        # types, we can save the form
        if form.is_valid():
            # saving the form creates a new User object and saves the User 
            # object to the database
            form.save()

            # now, we can log in the new user
            # request.POST is a dictionary
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            # just checking to see if the user exists for security reasons
            if user is not None:
                # log the user in using Django's built in login function
                login(request, user)
                # send them back to the home page
                return redirect("index")
            
    context = {"form": form}
    return render(request, "signup.html", context)

def login_(request):
    # set the webpage to look a certain way based on msg's value
    msg = ""
    # if a user tries to log in
    if request.method == 'POST':
        # grab the inputted username
        username = request.POST['username']
        # grab the inputted password
        password = request.POST['password']
        # let's attempt to grab the matching user from our database
        user = authenticate(request, username=username, password=password)
        # if the user exists
        if user is not None:
            # log him in
            login(request, user)
            # if the user is trying to go to a certain page
            if "next" in request.POST:
                # redirect him to that page
                return redirect(request.POST.get("next"))
            # otherwise, take him to the home page
            return redirect("index")
        else:
            # wrong log in information
            msg = "invalid credentials"
    context = {"msg": msg}
    return render(request, "login.html", context)
    
def logout_(request):
    # just log out the user
    logout(request)
    # and take them back home
    return redirect("index")

# the view function for handling the create poll page
@login_required(login_url="login")
def create(request):
    if request.method == 'POST':
        # grab the poll question
        question = request.POST.get("question")
        # grab the poll title
        title = request.POST.get("title")
        # grab the maker of the poll
        owner = request.user
        # create the poll
        poll = Poll.objects.create(question=question, title=title, owner=owner)
        # grab the options
        options = request.POST.getlist("options")
        # for each option
        for option in options:
            # create the option
            Option.objects.create(name=option, poll=poll)
        # send the user to the poll's vote page
        return redirect("vote", slug=poll.slug)
    # if the user hasn't submitted the form yet, show them the create poll page
    return render(request, "create.html")

# if the user isn't logged in, send him to the login page
@login_required(login_url="login")
def vote(request, slug):
    # Grab the Poll that matches the url name
    poll = Poll.objects.get(slug=slug)
    # Grab the options for this poll
    options = Option.objects.filter(poll=poll)

    # using a variable allows us to dynamically change the webpage from the
    # front end (in the template)
    msg = None

    # if the user is logged in
    if request.user.is_authenticated:
        # if the logged in user has already voted for this poll,
        # his name/id will match one of the voter ids connected with the poll
        # model
        if poll.voters.filter(id=request.user.id).exists():
            msg = "voted"

    # we got an input
    if request.method == 'POST':
        # let's say a user votes on this poll
        if 'vote' in request.POST:
            # Get the name of the selected option
            selected_option = request.POST.get("option")
            # Just checking on the terminal that we got the right option
            print(selected_option)
            # Get the actual option object
            option = Option.objects.get(id=selected_option)
            # add to the option's vote count
            option.total_vote += 1

            # get the poll for that option
            poll = option.poll
            # add to its vote count
            poll.total_vote += 1

            # record the voter for the option
            option.voters.add(request.user)
            # record the voter for the poll
            poll.voters.add(request.user)

            # save our changes
            option.save()
            poll.save()

        # if the owner of the poll tries to delete the poll
        elif 'delete_poll' in request.POST and request.user == poll.owner:
            # delete it from the database
            poll.delete()
            # take them back home
            return redirect("index")
        
        # show them the results page now
        return redirect("results", slug=poll.slug)
    
    # grab the poll, its options, and msg for the web page
    context = {"poll": poll, "options": options, "msg": msg}
    # show the user the vote webpage
    return render(request, "vote.html", context)

"""REMINDER: Add a delete button on the results page """
def results(request, slug):
    poll = Poll.objects.get(slug=slug)

    if request.method == "POST" and request.user == poll.owner:
        poll.delete()
        return redirect("index")
    
    options = Option.objects.filter(poll=poll)
    context = {"poll": poll, "options": options}
    
    return render(request, "results.html", context)
