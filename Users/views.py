import os
import json
import datetime
from pathlib import Path
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def SignUp(request):
    conditions = {
        'login': False
    }

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        dob_year = int(request.POST['dob-year'])
        dob_month = int(request.POST['dob-month'])
        dob_day = int(request.POST['dob-day'])

        date = datetime.date(dob_year, dob_month, dob_day)
        profile_image_path = request.FILES['uploaded-profile-image']

        gender = request.POST['gen']

        newUser = CustomUser(
            email=email,
            Gender=gender,
            DOB=date,
            ProfileImage=profile_image_path
        )

        newUser.set_password(password)
        newUser.save()

        user = authenticate(request, email=email, password=password)
        login(request, user)

        return redirect('/dashboard')

    return render(request, 'Signup.html', conditions)


def Login(request):
    if request.user.id is None:
        conditions = {
            'login': True
        }

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                if user.is_superuser:
                    return redirect('/admin')

                return redirect('/dashboard')

            else:
                messages.error(request, 'Email and Password did not match')

    else:
        return redirect('/dashboard')

    return render(request, 'Signup.html', conditions)


def Index(request):
    details = {
        'request': request,
    }

    if request.user.id:
        details.update({'nav_template': 'WelcomeNav.html'})

    else:
        details.update({'nav_template': 'IndexNav.html'})

    return render(request, 'index.html', details)


def TakeModelTest(request):
    questions = dict()

    BASE_DIR = Path(__file__).resolve().parent.parent
    jsonPath = os.path.join(BASE_DIR, 'static', 'Questions.json')

    with open(jsonPath) as f:
        contents = json.load(f)

    # all_contents = contents['BCA']['English']
    # all_contents.update(contents['BCA']['Math'])

    # for i in range(200):
    #     all_keys = list(all_contents.keys())
    #     question = random.choice(all_keys)

    #     questions[question] = all_contents[question]['choices']
    #     all_contents.pop(question)

    all_contents = contents['BCA']['Math']

    for question, values in all_contents.items():
        questions[question] = values['choices']

    values = {
        'nums': list(range(100)),
        'questions': questions
    }

    return render(request, 'ModelTest.html', values)


def DashBoard(request):
    print(request.user.ProfileImage)
    if request.user.id:
        return render(request, 'DashBoard.html')

    else:
        return redirect('login')


def Logout(request):
    logout(request)

    return redirect('index')
