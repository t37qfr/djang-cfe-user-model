from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, get_user_model, logout

from .forms import UserCreationForm, UserChangeForm, UserLoginForm

User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        pass
    return render(request, 'accounts/home.html', {})


def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
       form.save()
       return HttpResponseRedirect('/login')
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data.get('user_obj')
        #user = User.objects.get(username=username)
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')