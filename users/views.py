from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .models import *


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            ProfileModel.objects.create(user=user)
            login(request, user)
            return redirect('blog-home')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def profile_view(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'users/profile.html', context)
