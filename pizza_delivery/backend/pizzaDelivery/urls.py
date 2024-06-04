from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profile/', views.profilePage, name="profile"),
    path('profile/update-profile/', views.updateProfile, name="update_profile"),
    path('pizza/buy/', views.pizzaBuy, name="buy_pizza"),
    path('pizza/buy/payment-initiator/', views.paymentInitiator, name="payment_initiator"),
    path('pizza/buy/paymenthandler/', views.paymentHandler, name="payment-handler"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)