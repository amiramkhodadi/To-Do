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
        return redirect("signup")

    return render(request, "todo/signup.html", {})
