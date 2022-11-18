from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages

from .forms import UserRegisterForm
# Views
@login_required
def home(request):
    return render(request, "accueil.html", {})
 
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                isStaff = data.get('checkBoxInput')
                if isStaff:
                    instance = form.save(commit=False)  # get the model instance from the filled-out form without saving it to the database
                    instance.is_staff = True  # modify the instance by changing the is_staff attribute to True
                    instance.save()  # save the instance of the model to the database
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                firstname = form.cleaned_data.get('first_name')
                lastname = form.cleaned_data.get('last_name')
                user = authenticate(username = username, password = password, email = email, first_name = firstname, last_name = lastname)
                login(request, user)
                messages.success(request, "Register success." )

                return redirect('home')
        else:
            form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
