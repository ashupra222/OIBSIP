from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .utilFunctions import sendMail, generate_otp
import json

from django.contrib.auth import get_user_model
User = get_user_model()

def registerPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        otp = request.POST.get("otp")
        try:
            userobj = User.objects.get(username = username)
            if(userobj.verified):
                messages.success(request, "Already registerd. Login here", "registered")
                return redirect("login")
            elif (userobj.email != email):
                messages.info(request, "email does not match as previously registered", "registration_failed")
                return render(request, 'register.html', status=401)
            elif(int(otp) == userobj.otp):
                userobj.password = make_password(password)
                userobj.verified = True
                userobj.otp = None
                userobj.save()
                messages.success(request, "Registration done successfully.", "registered")
                return redirect("login")
            else:
                messages.info(request, "invalid otp", "registration_failed")
                return render(request, 'register.html', status=401)
        except:
            messages.info(request, "please generate otp first", "registration_failed")
            return render(request, 'register.html', status=401)
            
    return render(request, 'register.html')

def registerOtpGen(request):
    if request.method == "POST":
        try:
            email = json.loads(request.body).get("email")
            username = json.loads(request.body).get("username")
            if(email != "" and username != ""):
                otp = generate_otp()
                userobj, exist = User.objects.get_or_create(username=username)
                if(exist):
                    try:
                        userobj2 = User.objects.get(email=email)
                        if(not userobj2.verified):
                            userobj2.delete()
                            raise User.unique_error_message()
                        userobj.delete()
                        return JsonResponse("email already linked to another username,", safe=False)
                    except:
                        userobj.email = email
                        userobj.otp = otp
                        userobj.password = make_password(otp)
                        userobj.save()
                    
                
                elif(not userobj.verified):
                    userobj.email = email
                    userobj.otp = otp
                    userobj.password = make_password(otp)
                    userobj.save()
                    if(sendMail(email, otp)):
                        return JsonResponse("Email sent.", safe=False)
                    else:
                        return JsonResponse("Email can not be able to sent due to smtp error at server", safe=False)
                else:
                    return JsonResponse("username already exist", safe=False)
                if(sendMail(email, otp)):
                    return JsonResponse("Email sent.", safe=False)
                else:
                    return JsonResponse("Email can not be able to sent due to smtp error at server", safe=False)
            else:
                return JsonResponse("Email and username cannot be empty!", safe=False)
        except:
            print("an error")
        return JsonResponse("an server side error occured", safe=False)

def loginPage(request):
    if(request.method == "POST"):
        uname_or_email = request.POST.get("username")
        password = request.POST.get("password")
        userobj = None
        try:
            userobj = User.objects.get(username = uname_or_email)
        except:
            pass
        if(userobj is None):
            try:
                userobj = User.objects.get(email = uname_or_email)
            except:
                return render(request,
                          "message.html",
                          {"heading": "Not Registered",
                           "message": "The username or email is not registered",
                           "button": "Back"},
                           status=401)
        if(userobj is not None):
            if(check_password(password, userobj.password)):
                login(request, userobj)
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return render(request,
                          "message.html",
                          {"heading": "Login Succesfull",
                           "message": "you are logged in",
                           "button": "Continue"},
                           status=202)
            else:
                return render(request,
                          "message.html",
                          {"heading": "Invalid Credential",
                           "message": "The password is wrong",
                           "button": "Try Again"},
                           status=401)

    return render(request, "login.html")

def forgotPassPage(request):
    if(request.method == "POST"):
        uname_or_email = request.POST.get("uname_email")
        otp = request.POST.get("otp")
        userobj = None
        try:
            userobj = User.objects.get(username = uname_or_email)
        except:
            pass
        if(userobj is None):
            try:
                userobj = User.objects.get(email = uname_or_email)
            except:
                return render(request,
                          "message.html",
                          {"heading": "Not Registered",
                           "message": "The username or email is not registered",
                           "button": "Back"},
                           status=401)
        
        if(userobj is not None):
            if(int(otp) == userobj.otp):
                login(request, userobj)
                userobj.otp = None
                userobj.save()
                return redirect("change_pass")
            else:
                return render(request,
                          "message.html",
                          {"heading": "Invalid OTP",
                           "message": "The otp is wrong",
                           "button": "Try Again"},
                           status=401)

    return render(request, "forgotpass.html")

def forgotOtpGen(request):
    if request.method == "POST":
        try:
            uname_or_email = json.loads(request.body).get("uname_email")
            if(uname_or_email != "" ):
                otp = generate_otp()
                userobj = None
                try:
                    userobj = User.objects.get(username = uname_or_email)
                except:
                    pass
                if(userobj is None):
                    try:
                        userobj = User.objects.get(email = uname_or_email)
                    except:
                        return JsonResponse("username or email does not exist.", safe=False)
                
                if(userobj.verified):
                    userobj.otp = otp
                    userobj.save()
                    if(sendMail(userobj.email, otp)):
                        return JsonResponse("Email sent.", safe=False)
                    else:
                        return JsonResponse("Email can not be able to sent due to smtp error at server", safe=False)
                else:
                    return JsonResponse("user is not verified. First register the user properly", safe=False)
            else:
                return JsonResponse("Email and username cannot be empty!", safe=False)
        except json.decoder.JSONDecodeError:
            print("Decode Error")
        return JsonResponse("an server side error occured", safe=False)

@login_required(login_url="login")
def changePassPage(request):
    if(request.method == "POST" and request.user.is_authenticated):
        curr_user = request.user
        password = request.POST.get("password1")

        curr_user.password = make_password(password)
        curr_user.save()
        logout(request)
        messages.success(request, "password changed successfully.", "changePass")
        return redirect("login")
        
    return render(request, "changepass.html")

def logoutPage(request):
    logout(request)
    return redirect("login")