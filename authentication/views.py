from django.contrib.auth import (
    authenticate,
    login,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from common.decorators import public
from .forms import UserProfileForm
from .models import UserProfile


@public
def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile', pk=user.pk)
    else:
        form = UserCreationForm()

    return render(request, 'sign_up.html', {'form': form})


@public
def log_in(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dash')
        else:
            error = 'The credentials you entered are not valid. Try again.'

    return render(request, 'login.html', {'error': error})


@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user.userprofile
        )
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return redirect('profile', pk=user.pk)
    else:
        form = UserProfileForm(instance=user.userprofile)

    return render(request, 'profile_update.html', {
     'form': form,
     'user': user,
    })


@login_required
def profile(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    return render(request, 'profile.html', {'target_user': target_user})
