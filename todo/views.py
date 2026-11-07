from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .models import TODOO

TITLE_MAX_LENGTH = TODOO._meta.get_field("title").max_length
ALLOW_GET_FOR_DELETE_AND_LOGOUT = True


def _method_ok(request):
    return request.method == "POST" or ALLOW_GET_FOR_DELETE_AND_LOGOUT


def signup(request):
    if request.user.is_authenticated:
        return redirect("todo")

    if request.method == "POST":
        username = (request.POST.get("fnm") or "").strip()
        email = (
            (request.POST.get("email") or request.POST.get("emailid") or "")
            .strip()
            .lower()
        )
        password = request.POST.get("pwd") or ""
        password2 = request.POST.get("pwd2")

        errors = []

        if not username or not email or not password:
            errors.append("همه فیلدها را پر کنید.")
        else:
            if len(username) > 150:
                errors.append("نام کاربری نباید بیشتر از ۱۵۰ کاراکتر باشد.")

            try:
                validate_email(email)
            except ValidationError:
                errors.append("ایمیل وارد شده معتبر نیست.")

            if User.objects.filter(username__iexact=username).exists():
                errors.append("این نام کاربری قبلاً ثبت شده است.")

            if User.objects.filter(email__iexact=email).exists():
                errors.append("این ایمیل قبلاً ثبت شده است.")

            if password2 is not None and password != password2:
                errors.append("رمز عبور و تکرار آن یکسان نیستند.")

            try:
                validate_password(password, user=User(username=username, email=email))
            except ValidationError as e:
                errors.extend(e.messages)

        if not errors:
            try:
                User.objects.create_user(
                    username=username, email=email, password=password
                )
            except IntegrityError:
                errors.append("این نام کاربری قبلاً ثبت شده است.")
            else:
                messages.success(request, "ثبت‌نام انجام شد. اکنون وارد شوید.")
                return redirect("loginn")

        for err in errors:
            messages.error(request, err)

        return render(request, "todo/signup.html", {"fnm": username, "email": email})

    return render(request, "todo/signup.html", {})


def loginn(request):
    if request.method == "POST":
        username = request.POST.get("fnm")
        password = request.POST.get("pwd")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("todo")
        messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
        return redirect("loginn")

    return render(request, "todo/loginn.html", {})


@login_required(login_url="loginn")
def todo(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        if not title:
            messages.error(request, "عنوان نمی‌تواند خالی باشد.")
        elif len(title) > TITLE_MAX_LENGTH:
            messages.error(
                request, f"عنوان نباید بیشتر از {TITLE_MAX_LENGTH} کاراکتر باشد."
            )
        else:
            TODOO.objects.create(title=title, user=request.user)
        return redirect("todo")

    res = TODOO.objects.filter(user=request.user).order_by("-date")
    return render(request, "todo/todo.html", {"res": res})


def signout(request):
    if not _method_ok(request):
        return HttpResponseNotAllowed(["POST"])
    logout(request)
    return redirect("loginn")


@login_required(login_url="loginn")
def edit_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        if not title:
            messages.error(request, "عنوان نمی‌تواند خالی باشد.")
            return render(request, "todo/edit_todo.html", {"obj": obj})
        if len(title) > TITLE_MAX_LENGTH:
            messages.error(
                request, f"عنوان نباید بیشتر از {TITLE_MAX_LENGTH} کاراکتر باشد."
            )
            return render(request, "todo/edit_todo.html", {"obj": obj})
        obj.title = title
        obj.save()
        return redirect("todo")

    return render(request, "todo/edit_todo.html", {"obj": obj})


@login_required(login_url="loginn")
def delete_todo(request, srno):
    if not _method_ok(request):
        return HttpResponseNotAllowed(["POST"])
    obj = get_object_or_404(TODOO, srno=srno, user=request.user)
    obj.delete()
    return redirect("todo")
