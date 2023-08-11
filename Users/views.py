import json
import random
import datetime
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from .models import Programme, Subject, Questions, CustomUser, Exams, ResultDetails, FeedBack


def SignUp(request):
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
        return redirect('AdminIndex')

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
                    return redirect('AdminIndex')

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
        return redirect('AdminIndex')

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
        return redirect('AdminIndex')

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
        return redirect('AdminIndex')

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
        return redirect('AdminIndex')

    user = CustomUser.objects.get(id=request.user.id)
    user.ProfileImage = request.FILES['uploaded-profile-image']
    user.save()

    request.user.ProfileImage = CustomUser.objects.filter(id=request.user.id)[0].ProfileImage

    return redirect('go_to', redirect_to='profile')


def UpdatePassword(request):
    if request.user.is_superuser:
        return redirect('AdminIndex')

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
        return redirect('AdminIndex')

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
        ResultObj = Exams(UserID=UserObj, ProgrammeName=values[0]['program'])
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

    if request.user.is_superuser:
        Result = Exams.objects.filter(Slug=slug).first()

    else:
        Result = Exams.objects.filter(Slug=slug, UserID=request.user).first()

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
        return redirect('AdminIndex')

    return GoTo(request, 'dashboard')


def GetHistories(id):
    results = []

    for counter, result in enumerate(Exams.objects.filter(UserID=id)):
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
        return redirect('AdminIndex')

    if redirect_to not in ['profile', 'history', 'dashboard']:
        raise Http404

    data = dict()
    data['redirect_to'] = redirect_to

    id = CustomUser.objects.filter(id=request.user.id).first()

    if id is None:
        request.session['next'] = redirect_to
        return redirect('login')

    if redirect_to == 'history':
        data['results'] = GetHistories(id)

    elif redirect_to == 'dashboard':
        data.update(GetGraphsData(id))

    return render(request, 'Dashboard.html', {'to': data})


def GetGraphsData(id):
    values = dict()
    results = Exams.objects.filter(UserID=id)

    correct_answers = []
    incorrect_answers = []
    program_counter = dict()

    for result in results:
        correct_counter = result.CorrectCounter

        correct_answers.append(correct_counter)
        incorrect_answers.append(100 - correct_counter)

        programme = result.ProgrammeName

        if programme in program_counter:
            program_counter[programme] += 1

        else:
            program_counter[programme] = 1

    values.update(
            {
                'Pie-Chart-correct-vs-incorrect': {
                    'title': 'Overall Correct v/s Incorrect Answer',
                    'data': [sum(correct_answers), sum(incorrect_answers)],
                    'labels': ['Correct Answer', 'Incorrect Answer'],
                },

                'Pie-Chart-each-programme': {
                    'title': 'Test taken per programme',
                    'data': list(program_counter.values()),
                    'labels': list(program_counter.keys())
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


def GetUserLists(request):
    userDetails = []

    for user in CustomUser.objects.all():
        id = user.id
        dob = user.DOB
        email = user.email
        gender = user.Gender
        password = user.password
        memberSince = user.MemberSince
        is_user_active = user.is_active
        is_user_super = user.is_superuser
        profileImagePath = user.ProfileImage

        if dob is None:
            dob = '-'

        if gender is None:
            gender = '-'

        else:
            gender = gender[0].upper()

        userDetails.append(
            {
                'ID': id,
                'Email': email,
                'DOB': dob,
                'Gender': gender,
                'Profile Image': profileImagePath,
                'Member Since': memberSince,
                'template_type': 'template::users',
                'Admin': is_user_super,
                'Active': is_user_active,
            }
        )

    return render(request, 'admin/index.html', {'data': userDetails})


def GetExamsLists(request):
    exam_details = []
    exams = Exams.objects.all()

    for exam in exams:
        id = exam.ID
        user = exam.UserID,
        programme_name = exam.ProgrammeName
        correct_counter = exam.CorrectCounter
        date = exam.Date

        exam_details.append(
            {
                'ID': (id, exam.Slug),
                'User': (user[0].email, user[0].id),
                'Programme Name': programme_name,
                'Total Correct Answered': correct_counter,
                'Date': date,
                'template_type': 'template::exams'
            }
        )

    return render(request, 'admin/index.html', {'data': exam_details})


def GetProgrammeLists(request):
    programmeLists = []

    for programme in Programme.objects.all():
        id = programme.ID
        name = programme.Name

        programmeLists.append(
            {
                'ID': id,
                'Name': name,
                'template_type': 'template::programmes',
            }
        )

    return render(request, 'admin/index.html', {'data': programmeLists})


def GetSubjectLists(request):
    subjectLists = []

    for subject in Subject.objects.all():
        id = subject.ID
        name = subject.Name
        programmeName = subject.ProgrammeID.Name

        subjectLists.append(
            {
                'ID': id,
                'Programme Name': programmeName,
                'Subject Name': name,
                'Total Questions To Select': subject.TotalQuestionsToSelect,
                'template_type': 'template::subjects',
            }
        )

    return render(request, 'admin/index.html', {'data': subjectLists})


def GetQuestionLists(request):
    questionsLists = []

    for question in Questions.objects.all():
        id = question.ID
        title = question.Title
        answer = question.Answer
        OptionOne = question.OptionOne
        OptionTwo = question.OptionTwo
        OptionThree = question.OptionThree
        OptionFour = question.OptionFour
        subjectName = question.SubjectID.Name

        questionsLists.append(
            {
                'ID': id,
                'Subject': subjectName,
                'Programme': question.SubjectID.ProgrammeID.Name,
                'Title': title,
                'Answer': answer,
                'Option One': OptionOne,
                'Option Two': OptionTwo,
                'Option Three': OptionThree,
                'Option Four': OptionFour,
                'template_type': 'template::questions',
            }
        )

    return render(request, 'admin/index.html', {'data': questionsLists})


def AdminChangePassword(request):
    data = [
        {
            'template_type': 'template::change-password'
        }
    ]

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password1']

        user = get_user_model().objects.get(email=request.user)

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)
            messages.success(request, 'Password Changed Successfully')

        else:
            messages.error(request, 'Old Password did not match')

    return render(request, 'admin/index.html', {'data': data})


def EditQuestions(request, id):
    question = Questions.objects.filter(ID=id).first()

    if request.method == 'POST':
        question.Title = request.POST['Title']
        question.Answer = request.POST['Answer']
        question.OptionOne = request.POST['Option One']
        question.OptionTwo = request.POST['Option Two']
        question.OptionThree = request.POST['Option Three']
        question.OptionFour = request.POST['Option Four']

        question.save()

        messages.success(request, 'Edit Successful')

    data = [
        {
            'ID': question.ID,
            'Title': question.Title,
            'Answer': question.Answer,
            'Option One': question.OptionOne,
            'Option Two': question.OptionTwo,
            'Option Three': question.OptionThree,
            'Option Four': question.OptionFour,
            'template_type': 'template::edit-question',
        }
    ]

    if request.method == "POST":
        return redirect('edit-question', id=question.ID)

    return render(request, 'admin/index.html', {'data': data})


def EditUsers(request, id):
    user = CustomUser.objects.filter(id=id).first()

    if request.method == 'POST':
        user.email = request.POST['Email']

        if user.Gender is not None:
            user.Gender = request.POST['Gender']

        if user.DOB is not None:
            user.DOB = datetime.datetime.strptime(request.POST['DOB'], '%Y-%m-%d').date()

        if 'uploaded-profile-image' in request.FILES:
            user.ProfileImage = request.FILES['uploaded-profile-image']

        user.save()

        messages.success(request, 'Edit Successful')

    data = [
        {
            'ID': user.id,
            'Email': user.email,
            'Gender': user.Gender if user.Gender else '-',
            'DOB': user.DOB.strftime("%Y-%m-%d") if user.DOB else '-',
            'ProfileImage': user.ProfileImage,
            'Member Since': str(user.MemberSince).split('+')[0][:-3],
            'template_type': 'template::edit-user',
            'is_superuser': user.is_superuser,
        }
    ]

    if request.method == 'POST':
        return redirect('edit-user', id=id)

    return render(request, 'admin/index.html', {'data': data})


def AddNewQuestion(request):
    if request.method == 'POST':
        question = Questions()

        question.Title = request.POST['Title']
        question.Answer = request.POST['Answer']
        question.OptionOne = request.POST['Option One']
        question.OptionTwo = request.POST['Option Two']
        question.OptionThree = request.POST['Option Three']
        question.OptionFour = request.POST['Option Four']

        question.save()
        messages.success(request, 'Question Added Successful')

    data = [
        {
            'Title': '',
            'Answer': '',
            'Option One': '',
            'Option Two': '',
            'Option Three': '',
            'Option Four': '',
            'template_type': 'template::add-new-question',
        }
    ]

    return render(request, 'admin/index.html', {'data': data})


def GetFeedbackLists(request):
    feedbackLists = []
    feedbacks = FeedBack.objects.all()

    for feedback in feedbacks:
        data = {
                'ID': feedback.ID,
                'Name': feedback.Name,
                'Email': feedback.Email,
                'Message': feedback.Message,
                'Date': feedback.Date,
                'Completed': feedback.IsMarked,
                'template_type': 'template::feedbacks',
            }

        feedbackLists.append(data)

    return render(request, 'admin/index.html', {'data': feedbackLists})


def EditFeedback(request, id):
    feedback = FeedBack.objects.filter(ID=id).first()

    if request.method == 'POST':
        feedback.Name = request.POST['Name']
        feedback.Email = request.POST['Email']
        feedback.Message = request.POST['Message']

        feedback.save()

    data = [
        {
            'ID': feedback.ID,
            'Name': feedback.Name,
            'Email': feedback.Email,
            'Message': feedback.Message,
            'Date': feedback.Date,
            'IsMarked': feedback.IsMarked,
            'template_type': 'template::edit-feedbacks',
        }
    ]

    return render(request, 'admin/index.html', {'data': data})


def MarkFeedBack(request, id):
    feedback = FeedBack.objects.filter(ID=id).first()
    feedback.IsMarked = True
    feedback.save()

    return redirect('edit-feedback', id=id)
