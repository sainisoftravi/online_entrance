import json
import random
import datetime
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from .models import Programme, Subject, Questions, CustomUser, Results, ResultDetails, FeedBack


def SignUp(request):
    if request.user.is_superuser:
        return redirect('/admin')

    conditions = {
        'login': False
    }

    if request.method == 'POST':
        email = request.POST['email']

        if CustomUser.objects.filter(email=email):
            messages.error(request, 'Email already exists')
            return redirect('signup')

        password = request.POST['new_password1']

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

        return redirect('/')

    return render(request, 'Signup.html', conditions)


def Login(request):
    redirect_url = request.session.get('next')

    if request.user.is_superuser:
        return redirect('/admin')

    if request.user.id is None:
        conditions = {
            'login': True
        }

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['new_password1']
            remember_me = request.POST.get('remember-me', False)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                if remember_me is False:
                    request.session.set_expiry(0)

                if user.is_superuser:
                    return redirect('/admin')

                if redirect_url:
                    del request.session['next'] # Clear the session variable
                    return redirect('go_to', redirect_to=redirect_url)

                elif 'detailed-history-slug' in request.session:
                    slug = request.session['detailed-history-slug']

                    del request.session['detailed-history-slug']
                    return redirect('detailed-history', slug=slug)

                return redirect('go_to', redirect_to='dashboard')

            else:
                messages.error(request, 'Email and Password did not match')
                return redirect('login')

    else:
        return redirect('go_to', redirect_to=redirect_url)

    return render(request, 'Signup.html', conditions)


def Index(request):
    details = {
        'request': request,
    }

    if request.user.is_superuser:
        return redirect('/admin')

    elif request.method == 'POST':
        name = request.POST['contact-name']
        email = request.POST['contact-email']
        message = request.POST['contact-message']

        feedback = FeedBack(
                        Name=name,
                        Email=email,
                        Message=message
                    )

        feedback.save()

        messages.success(request, 'Thank you for your feedback')

        return redirect('index')

    elif request.user.id:
        details.update({'nav_template': 'WelcomeNav.html'})

    else:
        details.update({'nav_template': 'IndexNav.html'})

    return render(request, 'index.html', details)


def TakeModelTest(request, program):
    global values

    if request.user.is_superuser:
        return redirect('/admin')

    values = []
    programme = Programme.objects.filter(Name=program)[0]

    for subject in Subject.objects.filter(ProgrammeID=programme):
        questions = list(Questions.objects.filter(SubjectID=subject))
        random.shuffle(questions)

        questions = questions[:subject.TotalQuestionsToSelect]

        for question in questions:
            choices = [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour]
            details = {
                'id': question.ID,
                'title': question.Title,
                'choices': choices,
                'answer': question.Answer,
                'checked': False,
                'program': program
            }

            values.append(details)

    return render(request, 'ModelTest.html', {'questions': values})


def ProgramSelector(request):
    if request.user.is_superuser:
        return redirect('/admin')

    if request.user.is_authenticated:
        allPrograms = []

        for programObj in Programme.objects.all():
            allPrograms.append(programObj.Name)

        return render(request, 'ProgramSelector.html', {'programs': allPrograms})

    else:
        request.session['next'] = 'programselector'

        return redirect('login')


def UpdateProfile(request):
    if request.user.is_superuser:
        return redirect('/admin')

    user = CustomUser.objects.get(id=request.user.id)
    user.ProfileImage = request.FILES['uploaded-profile-image']
    user.save()

    request.user.ProfileImage = CustomUser.objects.filter(id=request.user.id)[0].ProfileImage

    return redirect('go_to', redirect_to='profile')


def UpdatePassword(request):
    if request.user.is_superuser:
        return redirect('/admin')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password Changed Successfully')

        else:
            messages.error(request, 'Old Password did not matched')

        return redirect('go_to', redirect_to='profile')


def Logout(request):
    logout(request)

    return redirect('index')


def DeleteAccount(request):
    if request.user.is_superuser:
        return redirect('/admin')

    user = CustomUser.objects.get(id=request.user.id)
    user.is_active = False
    user.save()

    logout(request)

    return redirect('index')


def GetResult(request):
    correct_counter = 0

    for value in values:
        value['checked'] = True

    if request.method == 'POST':
        UserObj = CustomUser.objects.get(id=request.user.id)
        ResultObj = Results(UserID=UserObj, ProgrammeName=values[0]['program'])
        ResultObj.save()

        QuestionNumber = [int(choice.split()[-1]) - 1 for choice in request.POST.keys() if choice.startswith('choices')]

        for qn in QuestionNumber:
            option = int(request.POST[f'choices {qn + 1}']) - 1

            userAnswer = values[qn]['choices'][option]
            values[qn]['UserAnswer'] = userAnswer

            ResultDetailsObj = ResultDetails(
                                    ResultID = ResultObj,
                                    QuestionID = Questions.objects.get(ID=values[qn]['id']),
                                    UserAnswer = userAnswer
                                )
            ResultDetailsObj.save()

            if userAnswer == values[qn]['answer']:
                correct_counter += 1
                values[qn]['is_correct'] = True

            else:
                values[qn]['is_correct'] = False

        ResultObj.CorrectCounter = correct_counter
        ResultObj.save()

        remaining = set(range(1, len(values))) - set(QuestionNumber)

        for rem in remaining:
            userAnswer = '-'
            values[rem]['is_correct'] = False
            values[rem]['UserAnswer'] = userAnswer

            ResultDetailsObj = ResultDetails(
                                    ResultID = ResultObj,
                                    QuestionID = Questions.objects.get(ID=values[rem]['id']),
                                    UserAnswer = userAnswer
                                )
            ResultDetailsObj.save()

        values[0]['CorrectCounter'] = correct_counter

        return render(request, 'ModelTest.html', {'questions': values})


def DetailedHistory(request, slug):
    if request.user.is_authenticated is False:
        request.session['detailed-history-slug'] = slug

        return redirect('login')

    values = []
    Result = Results.objects.filter(Slug=slug, UserID=request.user).first()

    if Result is None:
        raise Http404('Result Not Found')

    ResultDetail = ResultDetails.objects.filter(ResultID=Result)

    for res in ResultDetail:
        Question = res.QuestionID
        Choices = [Question.OptionOne, Question.OptionTwo, Question.OptionThree, Question.OptionFour]

        userAnswer = res.UserAnswer

        details = {
            'checked': True,
            'choices': Choices,
            'title': Question.Title,
            'UserAnswer': userAnswer,
            'answer': Question.Answer,
            'question_id': Question.ID
        }

        values.append(details)

        if userAnswer == details['answer']:
            details['is_correct'] = True

        else:
            details['is_correct'] = False

    values[0]['CorrectCounter'] = Result.CorrectCounter

    return render(request, 'ModelTest.html', {'questions': values})


def Dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin')

    return GoTo(request, 'dashboard')


def GetHistories(id):
    results = []

    for counter, result in enumerate(Results.objects.filter(UserID=id)):
        res = {
            'Date': result.Date,
            'Slug': result.Slug,
            'Counter': counter + 1,
            'Program': result.ProgrammeName
        }

        results.append(res)

    return results


def GoTo(request, redirect_to):
    if request.user.is_superuser:
        return redirect('/admin')

    data = dict()
    data['redirect_to'] = redirect_to

    id = CustomUser.objects.filter(id=request.user.id).first()

    if id is None:
        request.session['next'] = redirect_to
        return redirect('login')

    if redirect_to == 'history':
        data['results'] = GetHistories(id)

    elif redirect_to == 'dashboard':
        data.update(GetWrongRights(id))

    return render(request, 'Dashboard.html', {'to': data})


def GetWrongRights(id):
    values = dict()
    results = Results.objects.filter(UserID=id)

    correct_answers = []
    incorrect_answers = []

    for result in results:
        correct_counter = result.CorrectCounter

        correct_answers.append(correct_counter)
        incorrect_answers.append(100 - correct_counter)

    values.update(
            {
                'Pie-Chart-correct-vs-incorrect': {
                    'title': 'Overall Correct v/s Incorrect Answer',
                    'data': [sum(correct_answers), sum(incorrect_answers)],
                    'labels': ['Correct Answer', 'Incorrect Answer'],
                },

                'Stacked-Bar-Chart-Results': {
                    'correct': correct_answers,
                    'incorrect': [-ans for ans in incorrect_answers],
                    'title': 'Correct v/s Incorrect Answer Per Result',
                    'x-axis-labels': [f'#{i + 1}' for i in range(len(correct_answers))],
                }
            }
    )

    if correct_answers:
        return {
            'data': json.dumps(values)
        }

    return {
        'data': None
    }


def GetSpecificQuestions(request, programme, subject):
    global values

    values = []
    programme = Programme.objects.filter(Name=programme).first()
    subject = Subject.objects.filter(ProgrammeID=programme, Name=subject).first()
    questions = list(Questions.objects.filter(SubjectID=subject))

    random.shuffle(questions)

    questions = questions[:100]

    for question in questions:
        for question in questions:
            choices = [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour]

            random.shuffle(choices)

            details = {
                'id': question.ID,
                'title': question.Title,
                'choices': choices,
                'answer': question.Answer,
                'checked': False,
            }

            values.append(details)

    return render(request, 'ModelTest.html', {'questions': values})
