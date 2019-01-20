from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
def loginView(request):
    next = request.GET['next']
    print(next)
    return render(request, 'accounts/login.html', {'next' : next})

def logging(request):
    username = request.POST.get('username')
    password = request.POST['password']
    next = request.POST.get('next')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(next)
    else:
        return render(request, 'accounts/login.html', {'next' : next})

def logoutView(request):
    logout(request)
    return redirect('/')
