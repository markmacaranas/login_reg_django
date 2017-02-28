from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    if "id" in request.session:
        return redirect('/success')
    return render(request, 'login/index.html')

def success(request):
    if "id" not in request.session:
        return redirect('/')
    try:
        user = User.objects.get(id=request.session["id"])
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, "User not found.")
        return redirect('/')
    return render(request, 'login/success.html', {"user":user})

def process(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        user_valid = User.objects.validate(request.POST)
        if user_valid[0] == True:
            request.session["id"] = user_valid[1].id
            return redirect('/success')
        else:
            for msg in user_valid[1]:
                messages.add_message(request, messages.INFO, msg)
            return redirect('/')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        user = User.objects.authenticate(request.POST)
        if user[0] == True:
            request.session["id"] = user[1].id
            return redirect('/success')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect('/')

def logout(request):
    if "id" in request.session:
        request.session.pop("id")
    return redirect('/')
