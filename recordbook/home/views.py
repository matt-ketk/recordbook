from .forms import CreateTeamForm, JoinTeamForm
from .models import User, Account, Team, Design

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

import random

def index(request):
    context = {}
    return render(request, 'home/index.html', context)

class Login(LoginView):
    template_name = 'home/log_in.html'
    authentication_form = AuthenticationForm
    redirect_field_name = 'homepage'
    redirect_authenticated_user = True

def log_out(request):
    logout(request)
    return redirect('index')

def register(request):
    context = {'create_team': '/register/create_team/', 'join_team': '/register/join_team/'}
    return render(request, 'home/register.html', context)

def create_team(request):
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            # Get attributes from the form
            team_name = form.cleaned_data['team_name']
            captain_username = form.cleaned_data['captain_username']
            captain_password = form.cleaned_data['captain_password']
            captain_email = form.cleaned_data['captain_email']
            captain_first_name = form.cleaned_data['captain_first_name']
            captain_last_name = form.cleaned_data['captain_last_name']
            join_code = generate_join_code()
            # Create the new team
            team = Team(name=team_name, join_code=join_code)
            team.save()
            # Create a new user and add attributes
            captain_user = User.objects.create_user(username=captain_username, password=captain_password)
            captain_user.email = captain_email
            captain_user.first_name = captain_first_name
            captain_user.last_name = captain_last_name
            captain_user.save()
            # Create a new account associated with the user
            captain = Account(user=captain_user, team=team, is_captain=True)
            captain.save()
            # Log in user and display the join code
            login(request, captain_user)
            context = {'success': True, 'form': form, 'join_code': join_code}
            return render(request, 'home/create_team.html', context)
        # If form is invalid
        context = {'success': False, 'form': form}
        return render(request, 'home/create_team.html', context)

    else:
        form = CreateTeamForm()
        context = {'success': False, 'form': form}
        return render(request, 'home/create_team.html', context)

def join_team(request):
    if request.method == "POST":
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            # Get attributes from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            join_code = form.cleaned_data['team_join_code']
            # Create a new user and add attributes
            user = User.objects.create_user(username=username, password=password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # Find the Team associated with the join code
            team = Team.objects.get(join_code=join_code)
            # Create a new account associated with the user
            account = Account(user=user, team=team, is_captain=False)
            account.save()

            # Log in user and redirect to homepage
            login(request, user)
            return redirect('homepage')
        # If form is invalid
        context = {'form': form}
        return render(request, 'home/join_team.html', context)

    else:
        form = JoinTeamForm()
        context = {'form': form}
        return render(request, 'home/join_team.html', context)

@login_required
def homepage(request):
    context = {}
    return render(request, 'home/homepage.html', context)

@login_required
def designs(request):
    context = {}
    return render(request, 'home/designs.html', context)

@login_required
def team(request):
    user = request.user
    account = user.account
    team = account.team
    captain = team.accounts.get(is_captain=True)
    designs = []
    for account in team.accounts.all():
        for design in account.designs.all():
            designs.append(design)

    context = {
    'request': request,
    'user': user,
    'team': team,
    'account': account,
    'captain': captain,
    'designs': designs
    }
    return render(request, 'home/team.html', context)

@login_required
def dataEntry(request):
    context = {}
    return render(request, 'home/dataEntry.html', context)

@login_required
def launches(request):
    context = {}
    return render(request, 'home/launches.html', context)

def generate_join_code():
    join_code = ''
    for i in range(8):
        join_code = join_code + str(random.randint(0,9))
    unique = True
    for team in Team.objects.all():
        if join_code == team.join_code:
            unique = False
            break
    if unique:
        return join_code
    else:
        return generate_join_code()
