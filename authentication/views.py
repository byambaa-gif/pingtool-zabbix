# authentication/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = None
        if "@" in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # Log the user in
            token, _ = Token.objects.get_or_create(user=user)
            if(token):
             return redirect('/upload')
            else:
                return redirect("/")

            # return render(
            #     request,
            #     "login.html",
            #     {
            #         "token": token.key,
            #         "user_id": user.id,
            #         "username": user.username,
            #         "superuser": user.is_superuser,
            #     },
            # )

        return render(
            request, "login.html", {"error": "Incorrect username or password."}
        )

    # Default response for GET requests
    return render(request, "login.html")
