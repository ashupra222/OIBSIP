from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required


def registerPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if(password1 == password2):
            userobj, notexist = User.objects.get_or_create(username=username)
            if notexist:
                userobj.password = make_password(password1)
                userobj.save()
            else:
                return HttpResponse("User Already exist")
            return HttpResponse("Registration Successful")
        else:
            return HttpResponse("Password does not match")
    return render(request, "register.html")

def loginPage(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        try:
            user = User.objects.get(username = uname)
        except :
            return HttpResponse("Username does not exist")
        if(check_password(request.POST.get("password1"), user.password)):
            login(request, user)
            return redirect("profile")
        else:
            return HttpResponse("Wrong Password")
    return render(request, "login.html")

@login_required(login_url='login')
def profile(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get("email")
        user = User.objects.get(username=uname)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()
        return redirect("profile")
    return render(request, "profile.html")

def logoutPage(request):
    logout(request)
    return redirect("login")