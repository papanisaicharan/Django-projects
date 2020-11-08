from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    # user want to send info - signup
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password1']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'UserName has already been taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match!'})
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    # user want to send info - login
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Username and password combination is incorrect!'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    # need to route to home page
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
