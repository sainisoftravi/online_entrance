import re
import json
import random
import datetime
import requests
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import update_session_auth_hash, get_user_model
from .models import Programme, Subject, Questions, CustomUser, Exams, ResultDetails, ReportQuestion, FeedBack
from .search import *


URL_NEXT = None
uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'


def PaginatePage(request, data, number_of_data=100):
    """
    Paginate a page of data based on the specified parameters

    Parameters:
        request (Request): The HTTP request object.
        data: The data to be paginated.
        number_of_data (int): Optional. The number of data items to display per page. Default is 100.
    """

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
    """
    Handle user sign-up requests
    """

    if request.method == 'POST':
        email = request.POST['email']

        if CustomUser.objects.filter(email=email):
            messages.error(request, 'Email already exists')
            return redirect('signup')

        full_name = request.POST['full_name']
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
            DOB=date,
            FullName=full_name
        )

        if profile_image_path:
            newUser.ProfileImage = profile_image_path

        newUser.set_password(password)
        newUser.save()

        user = authenticate(request, email=email, password=password)
        login(request, user)

        return redirect('/')

    return render(request, 'Signup.html',
                    {
                        'page_title': 'Signup',
                    }
            )


def Login(request):
    """
    Handle user login functionality
    """

    global URL_NEXT

    url_next = request.GET.get('next', None)

    if url_next:
        URL_NEXT = url_next.strip('/')

    if request.user.is_superuser:
        return redirect('admin-index')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['new_password1']
        remember_me = request.POST.get('remember-me', False)

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            if remember_me is False:
                request.session.set_expiry(0)

            if user.is_superuser:
                return redirect('admin-index')

            if URL_NEXT is None:
                return redirect('user-dashboard')

            slug = re.search(uuid_pattern, URL_NEXT)

            if slug:
                return redirect("detailed-history", slug=slug.group())

            return redirect(URL_NEXT)

        else:
            messages.error(request, 'Email and Password did not match')
            return redirect('login')

    return render(request, 'login.html',
                    {
                        'page_title': 'Login',
                    }
            )


def Index(request):
    """
    Handle requests to the index page
    """

    if request.user.is_superuser:
        """
        Redirect superusers to the admin index.
        """

        return redirect('admin-index')

    elif request.method == 'POST':
        """
        Process feedback submitted via POST request.
        """

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

    return render(request, 'index.html',
                    {
                        'request': request,
                        'page_title': 'Online Entrance Preparation'
                    }
            )


def TakeModelTest(request, program):
    """
    Render a model test page for a specified program
    """

    global values

    if request.user.is_superuser:
        return redirect('admin-index')

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
                        'nav_template': 'nav.html',
                        'page_title': f'{program} | Test Ongoing'
                    }
                )


@login_required(login_url='login')
def ProgramSelector(request):
    """
    View function for selecting a program.
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    if request.user.is_authenticated:
        allPrograms = []

        for programObj in Programme.objects.all():
            allPrograms.append(programObj.Name)

        return render(request, 'ProgramSelector.html',
                        {
                            'programs': allPrograms,
                            'page_title': 'Select Programme'
                        }
                )


def UpdateProfile(request):
    """
    Handle a request to update user profile information.
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    user = CustomUser.objects.get(id=request.user.id)
    user.ProfileImage = request.FILES['uploaded-profile-image']
    user.save()

    request.user.ProfileImage = CustomUser.objects.filter(id=request.user.id)[0].ProfileImage

    return redirect('user-profile')


def UpdatePassword(request):
    """
    Handle a request to update user login password information
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password Changed Successfully')

        else:
            messages.error(request, 'Old Password did not matched')

        return redirect('user-profile')


def Logout(request):
    """
    Handle user logout
    """

    logout(request)

    return redirect('index')


def DeleteAccount(request):
    """
    Handle the deletion of a user account.
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    user = CustomUser.objects.get(id=request.user.id)
    user.is_active = False
    user.save()

    logout(request)

    return redirect('index')


def GetResult(request):
    """
    Display store exam results
    """

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

        return redirect('detailed-history', slug=ResultObj.Slug)


def DetailedHistory(request, slug):
    """
    View function for displaying detailed exam history

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug identifier for the exam.
    """

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
                        'nav_template': nav_template,
                        'page_title': slug.capitalize(),
                        'template_type': 'template::exams',
                    }
            )


def GetHistories(request, id):
    """
    Retrieve history data for a specific user ID from the API.
    """

    results = requests.get(f'http://{request.get_host()}/api/histories/{id}').json()

    return PaginatePage(request, results)


@login_required(login_url='login')
def UserDashboard(request):
    """
    View function for the user dashboard

    If the user is a superuser, redirect to the admin index. Otherwise,
    retrieve graph data for the user and render the user dashboard.
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    data = GetGraphsData(request.user.id)

    return render(request, 'Dashboard.html',
                    {
                        'to': data,
                        'page_title': 'DashBoard',
                        'redirect_to': 'dashboard'
                    }
            )


@login_required(login_url='login')
def UserProfile(request):
    """
    View for rendering the user profile page

    If the user is a superuser, redirects to the admin index. Otherwise,
    renders the user profile page.
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    return render(request, 'Profile.html',
                    {
                        'page_title': 'Profile',
                        'redirect_to': 'profile',
                    }
            )


@login_required(login_url='login')
def UserHistory(request):
    """
    View for rendering the user history page

    If the user is a superuser, redirects to the admin index. Otherwise,
    renders the user history page.
    """

    if request.user.is_superuser:
        return redirect('admin-index')

    paginator, page_data, page = GetHistories(request, request.user.id)

    return render(request, 'History.html',
                    {
                        'results': page_data,
                        'paginator': paginator,
                        'page_title': 'History',
                        'redirect_to': 'history',
                        'prev_page_index': page - 1,
                        'next_page_index': page + 1,
                    }
            )


def GetGraphsData(id):
    """
    Retrieve exam-related data for generating graphs
    """

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
    """
    Retrieve specific questions based on the specified program and subject.
    """

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

    if request.user.is_superuser:
        nav_template = 'admin/nav.html'

    else:
        nav_template = 'nav.html'

    return render(request, 'ModelTest.html',
                    {
                        'questions': values,
                        'nav_template': nav_template,
                        'page_title': 'Specific Test Ongoing'
                    }
            )


def ReportQuestions(request, id):
    """
    View for reporting a question
    """

    question = Questions.objects.filter(ID=id).first()

    if request.method == 'POST':
        reportQuestion = ReportQuestion(
            UserID = request.user,
            QuestionID = question,
            Issue = request.POST['message']
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

    return render(request, 'ReportQuestion.html',
                    {
                        'data': data,
                        'page_title': 'Report Question'
                    }
            )


def DisplayReportedQuestion(request, id):
    """
    View for displaying reported question
    """

    reportedQuestion = ReportQuestion.objects.filter(ID=id).first()

    data = {
        'editable': False,
        'id': reportedQuestion.ID,
        'Message': reportedQuestion.Issue,
        'title': reportedQuestion.QuestionID.Title
    }

    return render(request, 'ReportQuestion.html',
                    {
                        'data': data,
                        'page_title': 'Reported Question'
                    }
            )


def GetUserLists(request, users=None):
    """
    Retrieve user lists based on the provided request and user data.
    """

    drop_down_options = ['Email', 'DOB', 'Gender', 'Member Since', 'Admin', 'Non-Admin', 'Active', 'Non-Active']

    if users is None:
        users = CustomUser.objects.all()

    elif len(users) == 0:
        return render(request, 'admin/Users.html',
                        {
                            'page_title': 'Users',
                            'data_details': 'No data found',
                            'search_form_url': 'user-search',
                            'template_type': 'template::users',
                            'drop_down_options': drop_down_options,
                            'data_details': 'No data found',
                        }
                )

    DATA = requests.get(f'http://{request.get_host()}/api/users').json()
    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/Users.html',
                {
                    'data': data,
                    'page_title': 'Users',
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
    """
    Retrieve and display a list of exams with optional filtering.
    """

    drop_down_options = ['User', 'Programme Name', 'Total Correct Answered', 'Date']

    if exams is None:
        exams = requests.get(f'http://{request.get_host()}/api/exams').json()

    elif len(exams) == 0:
        return render(request, 'admin/Exams.html',
                        {
                            'page_title': 'Exams',
                            'data_details': 'No data found',
                            'search_form_url': 'exam-search',
                            'template_type': 'template::exams',
                            'js_path': 'js/admin/ExamSearch.js',
                            'drop_down_options': drop_down_options
                        }
                    )

    paginator, data, page = PaginatePage(request, exams)

    return render(request, 'admin/Exams.html',
                {
                    'data': data,
                    'page_title': 'Exams',
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
    """
    Retrieve a list of programmes from an API and render them on a paginated HTML template.
    """

    DATA = requests.get(f'http://{request.get_host()}/api/programmes').json()
    paginator, data, page = PaginatePage(request, DATA)

    return render(request, 'admin/Programmes.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'page_title': 'Programmes',
                    'prev_page_index': page - 1,
                    'next_page_index': page + 1,
                    'jump_to_url': 'getProgrammeDetails',
                    'template_type': 'template::programmes'
                }
            )


def GetSubjectLists(request, subjects=None):
    """
    Retrieve and render a paginated list of subjects
    """

    drop_down_options = ['Programme Name', 'Subject Name', 'Total Questions To Select']

    if subjects is None:
        subjects = requests.get(f'http://{request.get_host()}/api/subjects').json()

    elif len(subjects) == 0:
        return render(request, 'admin/Subjects.html',
                        {
                            'page_title': 'Subjects',
                            'data_details': 'No data found',
                            'search_form_url': 'subject-search',
                            'template_type': 'template::subjects',
                            'js_path': 'js/admin/SubjectSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    paginator, data, page = PaginatePage(request, subjects)

    return render(request, 'admin/Subjects.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'page_title': 'Subjects',
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
    """
    Retrieve and paginate a list of questions.
    """

    drop_down_options = ['Subject', 'Programme', 'Title', 'Answer', 'Options']

    if questions is None:
        questions = requests.get(f'http://{request.get_host()}/api/questions').json()

    elif len(questions) == 0:
        return render(request, 'admin/Questions.html',
                        {
                            'page_title': 'Questions',
                            'data_details': 'No data found',
                            'search_form_url': 'question-search',
                            'template_type': 'template::questions',
                            'js_path': 'js/admin/QuestionSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    paginator, data, page = PaginatePage(request, questions)

    return render(request, 'admin/Questions.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'page_title': 'Questions',
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
    """
    Retrieve and display feedback lists based on the given parameters.
    """

    drop_down_options = ['Name', 'Email', 'Date', 'Message', 'Marked', 'Not-Marked']

    if feedbacks is None:
        feedbacks = requests.get(f'http://{request.get_host()}/api/feedbacks').json()

    elif len(feedbacks) == 0:
        return render(request, 'admin/Feedbacks.html',
                        {
                            'page_title': 'FeedBacks',
                            'data_details': 'No data found',
                            'search_form_url': 'feedback-search',
                            'template_type': 'template::feedbacks',
                            'js_path': 'js/admin/FeedbackSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    paginator, data, page = PaginatePage(request, feedbacks)

    return render(request, 'admin/Feedbacks.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'page_title': 'FeedBacks',
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
    """
    Retrieve and display a paginated list of reports
    """

    drop_down_options = ['User', 'Issue', 'Date', 'Question', 'Marked', 'Not-Marked']

    if reports is None:
        reports = requests.get(f'http://{request.get_host()}/api/reports').json()

    elif len(reports) == 0:
        return render(request, 'admin/Reports.html',
                        {
                            'page_title': 'Reports',
                            'data_details': 'No data found',
                            'search_form_url': 'report-search',
                            'template_type': 'template::reports',
                            'js_path': 'js/admin/ReportSearch.js',
                            'drop_down_options': drop_down_options
                        }
                )

    paginator, data, page = PaginatePage(request, reports)

    return render(request, 'admin/Reports.html',
                {
                    'data': data,
                    'paginator': paginator,
                    'page_title': 'Reports',
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
    """
    View for handling admin password change
    """

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

    data = {
        'Old Password': 'old_password',
        'New Password': 'new_password1',
        'Confirm New Password': 'new_password2'
    }

    return render(request, 'admin/ChangePassword.html',
                    {
                        'data': data,
                        'page_title': 'Update Password',
                        'template_type': 'template::change-password'
                    }
            )


def EditQuestions(request, id):
    """
    View for editing a specific question.
    """

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

    return render(request, 'admin/Add-Edit-Questions.html',
                    {
                        'data': data,
                        'page_title': f'{data[0]["Title"]}',
                        'template_type': 'template::edit-question',
                    }

            )


def DeleteQuestion(request, id):
    """
    View to delete desired question
    """

    question = Questions.objects.filter(ID=id).first()
    question.delete()

    return redirect('questions')


def EditUsers(request, id):
    """
    View to edit the details of specific user in admin template
    """

    user = CustomUser.objects.filter(id=id).first()

    if request.method == 'POST':
        user.email = request.POST['Email']
        user.FullName = request.POST['full_name']

        if user.Gender is not None:
            user.Gender = request.POST['Gender']

        if user.DOB is not None:
            user.DOB = datetime.datetime.strptime(request.POST['DOB'], '%Y-%m-%d').date()

        if 'uploaded-profile-image' in request.FILES:
            user.ProfileImage = request.FILES['uploaded-profile-image']

        user.save()

        messages.success(request, 'Edit Successful')

    DATA = requests.get(f'http://{request.get_host()}/api/users/{id}').json()

    for data in DATA:
        data['MemberSince'] = datetime.datetime.strptime(data['MemberSince'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%d %b %Y, %I:%M %p")

    return render(request, 'admin/Edit-User.html',
                    {
                        'data': data,
                        'page_title': f'{data["email"]}',
                        'template_type': 'template::edit-user',
                    }
            )


def EditSubject(request, id):
    """
    View to edit the details of specific subject in admin template
    """

    subject = Subject.objects.filter(ID=id).first()

    if request.method == 'POST':
        subject.TotalQuestionsToSelect = request.POST['Total Questions To Select']
        subject.save()

        messages.success(request, 'Edit Successful')

    data = requests.get(f'http://{request.get_host()}/api/subjects/{id}').json()[0]
    data = [
        {
            'ID': data['ID'],
            'Programme': data['programme_name'],
            'Subject':data['Name'],
            'Total Questions To Select': data['TotalQuestionsToSelect']
        }
    ]

    return render(request, 'admin/Edit-Subject.html',
                    {
                        'data': data,
                        'template_type': 'template::edit-subject',
                        'page_title': f'{data[0]["Programme"]} > {data[0]["Subject"]}'
                    }
            )


def AddQuestion(request):
    """
    View to add new question in admin template
    """

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

    return render(request, 'admin/Add-Edit-Questions.html',
                  {
                    'data': data,
                    'page_title': 'Add Question',
                    'template_type': 'template::add-new-question',
                  }
            )


def EditFeedback(request, id):
    """
    View to edit the details of specific feedback in admin template
    """

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

    return render(request, 'admin/Edit-Feedback.html',
                    {
                        'data': data,
                        'page_title': f'{data[0]["Message"]}',
                        'template_type': 'template::edit-feedbacks',
                    }
                )


def EditReports(request, id):
    """
    View to edit the details of specific report in admin template
    """

    data = requests.get(f'http://{request.get_host()}/api/reports/{id}').json()[0]

    return render(request, 'admin/Edit-Report.html',
                    {
                        'data': data,
                        'page_title': f'{data["Issue"]}',
                        'template_type': 'template::edit-reports'
                    }
                )


def MarkReport(request, id):
    """
    View for indicating that a particular report has been flagged or marked
    """

    reportedQuestion = ReportQuestion.objects.filter(ID=id).first()
    reportedQuestion.IsMarked = True
    reportedQuestion.save()

    messages.success(request, 'Report has been marked')

    return redirect('edit-report', id=id)


def MarkFeedBack(request, id):
    """
    View for indicating that a particular feedback has been flagged or marked
    """

    feedback = FeedBack.objects.filter(ID=id).first()
    feedback.IsMarked = True
    feedback.save()

    messages.success(request, 'Feedback has been read')

    return redirect('edit-feedback', id=id)


def UserSearch(request):
    """
    Perform user search based on specified criteria.
    """

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
    """
    Perform exam search based on specified criteria.
    """

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
    """
    Perform subject search based on specified criteria.
    """

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
    """
    Perform question search based on specified criteria.
    """

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
    """
    Perform report search based on specified criteria.
    """

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
    """
    Perform feedback search based on specified criteria.
    """

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
