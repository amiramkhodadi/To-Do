from django.urls import path

from .views import delete_todo, edit_todo, loginn, signout, signup, todo

urlpatterns = [
    path("", signup, name="signup"),
    path("loginn/", loginn, name="loginn"),
    path("todopage/", todo, name="todo"),
    path("signout/", signout, name="signout"),
    path("edit_todo/<int:srno>", edit_todo, name="edit_todo"),
    path("delete_todo/<int:srno>", delete_todo, name="delete_todo"),
]
