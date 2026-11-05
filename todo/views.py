from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import TODOO


# Create your views here.
def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("fnm")
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        # print(firstname, password, email)
        user = User.objects.create_user(firstname, email, password).save()
        return redirect("loginn")

    return render(request, "todo/signup.html", {})


def loginn(request):
    if request.method == "POST":
        firstname = request.POST.get("fnm")
        password = request.POST.get("pwd")
        print(firstname, password)
        user = authenticate(request, username=firstname, password=password)
        if user is not None:
            login(request, user)
            return redirect("/todopage")
        else:
            return redirect("loginn")

    return render(request, "todo/loginn.html", {})
