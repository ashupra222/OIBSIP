from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('register/otp-gen/', views.registerOtpGen, name="otp_gen"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('forget-pass/', views.forgotPassPage, name="forget_pass"),
    path('forget-pass/otp-gen/', views.forgotOtpGen, name="forgot_otp_gen"),
    path('change-pass/', views.changePassPage, name="change_pass"),
]