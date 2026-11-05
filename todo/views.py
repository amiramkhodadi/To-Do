from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import TODOO


# Create your views here.
def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("fnm")
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        user = User.objects.create_user(firstname, email, password).save()
        return redirect("loginn")

    return render(request, "todo/signup.html", {})


def loginn(request):
    if request.method == "POST":
        firstname = request.POST.get("fnm")
        password = request.POST.get("pwd")
        user = authenticate(request, username=firstname, password=password)
        if user is not None:
            login(request, user)
            return redirect("/todopage")
        else:
            return redirect("loginn")

    return render(request, "todo/loginn.html", {})


@login_required(login_url="/loginn")
def todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        print(title)
        obj = TODOO(title=title, user=request.user)
        obj.save()
        user = request.user
        res = TODOO.objects.filter(user=user).order_by("-date")
        return redirect("/todopage", {"res": res})

    res = TODOO.objects.filter(user=request.user).order_by("-date")
    return render(
        request,
        "todo/todo.html",
        {"res": res},
    )


def signout(request):
    logout(request)
    return redirect("/loginn")


@login_required(login_url="/loginn")
def edit_todo(request, srno):
    if request.method == "POST":
        title = request.POST.get("title")
        obj = TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect("/todopage")

    obj = TODOO.objects.get(srno=srno)
    return render(request, "todo/edit_todo.html", {"obj": obj})


@login_required(login_url="/loginn")
def delete_todo(request, srno):
    obj = TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect("/todopage")
