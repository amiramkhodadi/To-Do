from django.urls import path

from .views import loginn, signup, todo

urlpatterns = [
    path("", signup, name="signup"),
    path("loginn/", loginn, name="loginn"),
    path("todopage/", todo, name="todo"),
]
