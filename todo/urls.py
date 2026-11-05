from django.urls import path

from .views import loginn, signup

urlpatterns = [
    path("", signup, name="signup"),
    path("loginn/", loginn, name="loginn"),
]
