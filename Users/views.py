import json
import random
import datetime
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import update_session_auth_hash, get_user_model
from .models import Programme, Subject, Questions, CustomUser, Exams, ResultDetails, ReportQuestion, FeedBack
from .search import *


def PaginatePage(request, data, number_of_data=100):
    page = int(request.GET.get('pages', 1))
    paginator = Paginator(data, number_of_data)

    try:
        data = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        data = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        data = paginator.page(paginator.num_pages)

    return paginator, data, page


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

    return render(request, 'ModelTest.html',
                    {
                        'questions': values,
                        'nav_template': 'nav.html'
                    }
                )


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
            'id': Question.ID,
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

    if request.user.is_superuser:
        nav_template = 'admin/nav.html'

    else:
        nav_template = 'nav.html'

    return render(request, 'ModelTest.html',
                    {
                        'questions': values,
                        'nav_template': nav_template
                    }
            )


def Dashboard(request):
    if request.user.is_superuser:
        return redirect('AdminIndex')

    return GoTo(request, 'dashboard')


def GetHistories(id):
    results = []

    for result in Exams.objects.filter(UserID=id):
        res = {
            'Date': result.Date,
            'Slug': result.Slug,
            'mark': result.CorrectCounter,
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


def ReportQuestions(request, id):
    question = Questions.objects.filter(ID=id).first()

    if request.method == 'POST':
        reportQuestion = ReportQuestion(
            UserID = request.user,
            QuestionID = question,
            Details = request.POST['message']
        )

        reportQuestion.save()

        messages.success(request, 'Sent your report to the developer(s)')
        return redirect('report-question-added', id=reportQuestion.ID)

    data = {
        'id': id,
        'editable': True,
        'title': question.Title,
        'options': [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour]
    }

    return render(request, 'ReportQuestion.html', {'data': data})


def DisplayReportedQuestion(request, id):
    reportedQuestion = ReportQuestion.objects.filter(ID=id).first()

    data = {
        'editable': False,
        'id': reportedQuestion.ID,
        'Message': reportedQuestion.Issue,
        'title': reportedQuestion.QuestionID.Title
    }

    return render(request, 'ReportQuestion.html', {'data': data})


def GetUserLists(request, users=None):
    DATA = []
    drop_down_options = ['Email', 'DOB', 'Gender', 'Member Since', 'Admin', 'Non-Admin', 'Active', 'Non-Active']

    if users is None:
        users = CustomUser.objects.all()

    elif len(users) == 0:
        return render(request, 'admin/index.html',
                        {
                            'js_path': 'js/admin/UserSearch.js',
                            'search_form_url': 'user-search',
                            'template_type': 'template::users',
                            'drop_down_options': drop_down_options,
                            'data_details': 'No data found',
                        }
                )

    for user in users:
        id = user.id
        email = user.email
        gender = user.Gender
        is_user_active = user.is_active
        is_user_super = user.is_superuser
        profileImagePath = user.ProfileImage

        DATA.append(
            {
                'ID': id,
                'Email': email,
                'Gender': gender,
                'ProfileImage': profileImagePath,
                'Admin': is_user_super,
                'Active': is_user_active,
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'search_form_url': 'user-search',
                    'jump_to_url': 'getUserDetails',
                    'template_type': 'template::users',
                    'js_path': 'js/admin/UserSearch.js',
                    'drop_down_options': drop_down_options
                }
            )


def GetExamsLists(request, exams=None):
    DATA = []
    drop_down_options = ['User', 'Programme Name', 'Total Correct Answered', 'Date']

    if exams is None:
        exams = Exams.objects.all()

    elif len(exams) == 0:
        return render(request, 'admin/index.html',
                        {
                            'data_details': 'No data found',
                            'search_form_url': 'exam-search',
                            'template_type': 'template::exams',
                            'js_path': 'js/admin/ExamSearch.js',
                            'drop_down_options': drop_down_options
                        }
                    )

    for exam in exams:
        DATA.append(
            {
                'date': exam.Date,
                'examSlug': exam.Slug,
                'email': exam.UserID.email,
                'programme': exam.ProgrammeName,
                'correct_counter': exam.CorrectCounter,
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getExamDetails',
                    'search_form_url': 'exam-search',
                    'template_type': 'template::exams',
                    'js_path': 'js/admin/ExamSearch.js',
                    'drop_down_options': drop_down_options,
                }
            )


def GetProgrammeLists(request):
    DATA = []

    for programme in Programme.objects.all():
        id = programme.ID
        name = programme.Name

        DATA.append(
            {
                'ID': id,
                'Name': name,
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getProgrammeDetails',
                    'template_type': 'template::programmes'
                }
            )


def GetSubjectLists(request, subjects=None):
    DATA = []
    drop_down_options = ['Programme Name', 'Subject Name', 'Total Questions To Select']

    if subjects is None:
        subjects = Subject.objects.all()

    elif len(subjects) == 0:
        return render(request, 'admin/index.html',
                        {
                            'data_details': 'No data found',
                            'search_form_url': 'subject-search',
                            'template_type': 'template::subjects',
                            'js_path': 'js/admin/SubjectSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    for subject in subjects:
        DATA.append(
            {
                'ID': subject.ID,
                'subject': subject.Name,
                'programme': subject.ProgrammeID.Name,
                'total_question': subject.TotalQuestionsToSelect
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getSubjectDetails',
                    'search_form_url': 'subject-search',
                    'template_type': 'template::subjects',
                    'drop_down_options': drop_down_options,
                    'js_path': 'js/admin/SubjectSearch.js',
                }
            )


def GetQuestionLists(request, questions=None):
    DATA = []
    drop_down_options = ['Subject', 'Programme', 'Title', 'Answer', 'Options']

    if questions is None:
        questions = Questions.objects.all()

    elif len(questions) == 0:
        return render(request, 'admin/index.html',
                        {
                            'data_details': 'No data found',
                            'search_form_url': 'question-search',
                            'template_type': 'template::questions',
                            'js_path': 'js/admin/QuestionSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    for question in questions:
        DATA.append(
            {
                'ID': question.ID,
                'title': question.Title,
                'answer': question.Answer,
                'subject': question.SubjectID.Name,
                'programme': question.SubjectID.ProgrammeID.Name,
                'options': [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour],
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getQuestionDetails',
                    'search_form_url': 'question-search',
                    'template_type': 'template::questions',
                    'js_path': 'js/admin/QuestionSearch.js',
                    'drop_down_options': drop_down_options
                }
            )


def GetFeedbackLists(request, feedbacks=None):
    DATA = []
    drop_down_options = ['Name', 'Email', 'Date', 'Message', 'Marked', 'Not-Marked']

    if feedbacks is None:
        feedbacks = FeedBack.objects.all()

    elif len(feedbacks) == 0:
        return render(request, 'admin/index.html',
                        {
                            'data_details': 'No data found',
                            'search_form_url': 'feedback-search',
                            'template_type': 'template::feedbacks',
                            'js_path': 'js/admin/FeedbackSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    for feedback in feedbacks:
        DATA.append(
            {
                'ID': feedback.ID,
                'name': feedback.Name,
                'date': feedback.Date,
                'email': feedback.Email,
                'message': feedback.Message,
                'completed': feedback.IsMarked,
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getFeedbacks',
                    'search_form_url': 'feedback-search',
                    'template_type': 'template::feedbacks',
                    'js_path': 'js/admin/FeedbackSearch.js',
                    'drop_down_options': drop_down_options
                }
            )


def GetReportsLists(request, reports=None):
    DATA = []
    drop_down_options = ['User', 'Issue', 'Date', 'Question', 'Marked', 'Not-Marked']

    if reports is None:
        reports = ReportQuestion.objects.all()

    elif len(reports) == 0:
        return render(request, 'admin/index.html',
                        {
                            'data_details': 'No data found',
                            'search_form_url': 'report-search',
                            'template_type': 'template::reports',
                            'js_path': 'js/admin/ReportSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    for report in reports:
        DATA.append(
            {
                'ID': report.ID,
                'date': report.Date,
                'issue': report.Issue,
                'fixed': report.IsMarked,
                'user': report.UserID.email,
                'question': report.QuestionID.Title
            }
        )

    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/index.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getReportsLists',
                    'search_form_url': 'report-search',
                    'template_type': 'template::reports',
                    'js_path': 'js/admin/ReportSearch.js',
                    'drop_down_options': drop_down_options
                }
            )


def AdminChangePassword(request):
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

    return render(request, 'admin/index.html', {'template_type': 'template::change-password'})


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
        }
    ]

    if request.method == "POST":
        return redirect('edit-question', id=question.ID)

    return render(request, 'admin/index.html',
                    {
                        'data': data,
                        'template_type': 'template::edit-question',
                    }

            )


def DeleteQuestion(request, id):
    question = Questions.objects.filter(ID=id).first()
    question.delete()

    return redirect('getQuestionDetails')


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

        return redirect('edit-user', id=id)

    data = [
        {
            'ID': user.id,
            'Email': user.email,
            'Gender': user.Gender if user.Gender else '-',
            'DOB': user.DOB.strftime("%Y-%m-%d") if user.DOB else '-',
            'ProfileImage': user.ProfileImage,
            'Member Since': str(user.MemberSince).split('+')[0][:-3],
            'is_superuser': user.is_superuser,
        }
    ]

    return render(request, 'admin/index.html',
                    {
                        'data': data,
                        'template_type': 'template::edit-user',
                    }
            )


def EditSubject(request, id):
    subject = Subject.objects.filter(ID=id).first()

    if request.method == 'POST':
        subject.TotalQuestionsToSelect = request.POST['Total Questions To Select']
        subject.save()

        messages.success(request, 'Edit Successful')

        return redirect('edit-subject', id=id)

    data = [
        {
            'ID': subject.ID,
            'Programme': subject.ProgrammeID,
            'Subject': subject.Name,
            'Total Questions To Select': subject.TotalQuestionsToSelect
        }
    ]

    return render(request, 'admin/index.html',
                    {
                        'data': data,
                        'template_type':
                        'template::edit-subject'
                    }
            )


def AddNewQuestion(request):
    if request.method == 'POST':
        programmeID = Programme.objects.filter(Name=request.POST['Programme']).first()
        SubjectID = Subject.objects.filter(ProgrammeID=programmeID, Name=request.POST['Subject']).first()

        question = Questions(SubjectID=SubjectID)

        question.Title = request.POST['Title']
        question.Answer = request.POST['Answer']
        question.OptionOne = request.POST['Option One']
        question.OptionTwo = request.POST['Option Two']
        question.OptionThree = request.POST['Option Three']
        question.OptionFour = request.POST['Option Four']

        question.save()
        messages.success(request, 'Question Added Successful')

    select_options = dict()

    for head in Programme.objects.all():
        tails = [tail.Name for tail in Subject.objects.filter(ProgrammeID=head)]
        select_options[head.Name] = tails

    select_options = json.dumps(select_options)
    data = [
        {
            'SelectOptions': select_options,
            'Title': '',
            'Answer': '',
            'Option One': '',
            'Option Two': '',
            'Option Three': '',
            'Option Four': ''
        }
    ]

    return render(request, 'admin/index.html',
                  {
                      'data': data,
                      'template_type': 'template::add-new-question',
                  }
            )


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
        }
    ]

    return render(request, 'admin/index.html',
                    {
                        'data': data,
                        'template_type': 'template::edit-feedbacks'
                    }
                )


def EditReports(request, id):
    reportedQuestion = ReportQuestion.objects.filter(ID=id).first()

    data = [
        {
            'ID': reportedQuestion.ID,
            'User': reportedQuestion.UserID.email,
            'Issue': reportedQuestion.Issue,
            'Question': (reportedQuestion.QuestionID, reportedQuestion.QuestionID.Title),
            'Date': reportedQuestion.Date,
            'Fixed': reportedQuestion.IsMarked,
        }
    ]

    return render(request, 'admin/index.html',
                    {
                        'data': data,
                        'template_type': 'template::edit-reports',
                    }
                )


def MarkReport(request, id):
    reportedQuestion = ReportQuestion.objects.filter(ID=id).first()
    reportedQuestion.IsMarked = True
    reportedQuestion.save()

    return redirect('edit-report', id=id)


def MarkFeedBack(request, id):
    feedback = FeedBack.objects.filter(ID=id).first()
    feedback.IsMarked = True
    feedback.save()

    return redirect('edit-feedback', id=id)


def UserSearch(request):
    searching_type = request.GET.get('search-type')
    searching_value = request.GET.get('search-value')

    usrSearch = UserFilter(searching_value)

    maps = {
        'dob': lambda: usrSearch.SearchByDOB(),
        'email': lambda: usrSearch.SearchByEmail(),
        'admin': lambda: usrSearch.SearchByAdmin(),
        'gender': lambda: usrSearch.SearchByGender(),
        'active': lambda: usrSearch.SearchByActive(),
        'member since': lambda: usrSearch.SearchByMemberSince(),
        'non-admin': lambda: usrSearch.SearchByAdmin(is_admin=False),
        'non-active': lambda: usrSearch.SearchByActive(is_active=False),
    }

    users = maps.get(searching_type.lower(), None)

    if users:
        users = users()

    return GetUserLists(request, users=users)


def ExamSearch(request):
    searching_type = request.GET.get('search-type')
    searching_value = request.GET.get('search-value')

    examSearch = ExamFilter(searching_value)

    maps = {
        'date': lambda: examSearch.SearchByDate(),
        'user': lambda: examSearch.SearchByUser(),
        'programme name': lambda: examSearch.SearchByProgrammeName(),
        'total correct answered': lambda: examSearch.SearchByTotalCorrectAnswer(),
    }

    exams = maps.get(searching_type.lower(), None)

    if exams:
        exams = exams()

    return GetExamsLists(request, exams=exams)


def SubjectSearch(request):
    searching_type = request.GET.get('search-type')
    searching_value = request.GET.get('search-value')

    subjectSearch = SubjectFilter(searching_value)

    maps = {
        'subject name': lambda: subjectSearch.SearchBySubjectName(),
        'programme name': lambda: subjectSearch.SearchByProgrammeName(),
        'total questions to select': lambda: subjectSearch.SearchByTotalQuestionsToSelect()
    }

    subjects = maps.get(searching_type.lower(), None)

    if subjects:
        subjects = subjects()

    return GetSubjectLists(request, subjects=subjects)


def QuestionSearch(request):
    searching_type = request.GET.get('search-type').strip()
    searching_value = request.GET.get('search-value').strip()

    questionSearch = QuestionFilter(searching_value)

    maps = {
        'subject': lambda: questionSearch.SearchBySubject(),
        'programme': lambda: questionSearch.SearchByProgramme(),
        'title': lambda: questionSearch.SearchByTitle(),
        'answer': lambda: questionSearch.SearchByAnswer(),
        'options': lambda: questionSearch.SearchByOptions()
    }

    questions = maps.get(searching_type.lower(), None)

    if questions:
        questions = questions()

    return GetQuestionLists(request, questions=questions)


def ReportSearch(request):
    searching_type = request.GET.get('search-type').strip()
    searching_value = request.GET.get('search-value').strip()

    reportSearch = ReportFilter(searching_value)

    maps = {
        'user': lambda: reportSearch.SearchByUser(),
        'date': lambda: reportSearch.SearchByDate(),
        'issue': lambda: reportSearch.SearchByIssue(),
        'marked': lambda: reportSearch.SearchByMarked(),
        'question': lambda: reportSearch.SearchByQuestion(),
        'not-marked': lambda: reportSearch.SearchByMarked(is_marked=False),
    }

    reports = maps.get(searching_type.lower(), None)

    if reports:
        reports = reports()

    return GetReportsLists(request, reports=reports)


def FeedbackSearch(request):
    searching_type = request.GET.get('search-type').strip()
    searching_value = request.GET.get('search-value').strip()

    feedbackSearch = FeedbackFilter(searching_value)

    maps = {
        'name': lambda: feedbackSearch.SearchByName(),
        'date': lambda: feedbackSearch.SearchByDate(),
        'email': lambda: feedbackSearch.SearchByEmail(),
        'marked': lambda: feedbackSearch.SearchByMarked(),
        'message': lambda: feedbackSearch.SearchByMessage(),
        'not-marked': lambda: feedbackSearch.SearchByMarked(is_marked=False),
    }

    feedbacks = maps.get(searching_type.lower(), None)

    if feedbacks:
        feedbacks = feedbacks()

    return GetFeedbackLists(request, feedbacks=feedbacks)
