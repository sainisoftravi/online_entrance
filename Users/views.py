import random
import datetime
from .models import CustomUser
from django.conf import Settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from .models import Programme, Subject, Questions, CustomUser


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

        gender = request.POST['gen']
        date = datetime.date(dob_year, dob_month, dob_day)

        if 'uploaded-profile-image' in request.FILES:
            profile_image_path = request.FILES['uploaded-profile-image']

        else:
            profile_image_path = None

        newUser = CustomUser(
            email=email,
            Gender=gender,
            DOB=date
        )

        if profile_image_path:
            newUser.ProfileImage = profile_image_path

        newUser.set_password(password)
        newUser.save()

        user = authenticate(request, email=email, password=password)
        login(request, user)

        return redirect('/profile')

    return render(request, 'Signup.html', conditions)


def Login(request):
    if request.user.id is None:
        conditions = {
            'login': True
        }

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            remember_me = request.POST.get('remember-me', False)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                if remember_me is False:
                    request.session.set_expiry(0)

                if user.is_superuser:
                    return redirect('/admin')

                redirect_url = request.session.get('next', '/')

                if 'next' in request.session:
                    del request.session['next'] # Clear the session variable

                return redirect(redirect_url)

            else:
                messages.error(request, 'Email and Password did not match')

    else:
        return redirect('/profile')

    return render(request, 'Signup.html', conditions)


def Index(request):
    details = {
        'request': request,
    }

    if request.user.is_superuser:
        return redirect('/admin')

    elif request.user.id:
        details.update({'nav_template': 'WelcomeNav.html'})

    else:
        details.update({'nav_template': 'IndexNav.html'})

    return render(request, 'index.html', details)


def TakeModelTest(request, program):
    tests = []
    values = dict()
    programme = Programme.objects.filter(Name=program)[0]

    for subject in Subject.objects.filter(ProgrammeID=programme):
        questions = list(Questions.objects.filter(SubjectID=subject))
        random.shuffle(questions)

        questions = questions[:subject.TotalQuestionsToSelect]

        for question in questions:
            choices = [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour]
            random.shuffle(choices)

            details = {
                'id': question.ID,
                'title': question.Title,
                'choices': choices
            }

            tests.append(details)

    for test in tests:
        values[test['title']] = test['choices']

    return render(request, 'ModelTest.html', {'questions': values})


def ProgramSelector(request):
    if request.user.is_authenticated:
        allPrograms = []

        for programObj in Programme.objects.all():
            allPrograms.append(programObj.Name)

        return render(request, 'ProgramSelector.html', {'programs': allPrograms})

    else:
        request.session['next'] = 'programselector'
        return redirect('login')


def Profile(request):
    print(request.user.ProfileImage)
    if request.user.id:
        return render(request, 'Profile.html')

    else:
        return redirect('login')


def UpdateProfile(request):
    user = CustomUser.objects.get(id=request.user.id)
    user.ProfileImage = request.FILES['uploaded-profile-image']
    user.save()

    return redirect('/profile')


def UpdatePassword(request):
    user = CustomUser.objects.get(id=request.user.id)

    old_password_encrypted = user.password
    old_password = request.POST['OldPassword']

    if check_password(old_password, old_password_encrypted):
        new_password = request.POST['NewPassword']
        user.set_password(new_password)

        messages.success(request, 'Password Changed Successfully')

    else:
        messages.error(request, 'Old Password did not matched')

    return redirect('profile')


def Logout(request):
    logout(request)

    return redirect('index')


def DeleteAccount(request):
    user = CustomUser.objects.get(id=request.user.id)
    user.is_active = False
    user.save()

    logout(request)

    return redirect('index')
