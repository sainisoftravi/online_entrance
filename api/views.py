from Users.models import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class Users(APIView):
    """
    API View for retrieving user information

    Endpoint:
        GET api/users/<get_by (optional)>: Retrieve a list of all users or a specific user by email or ID

    Parameters:
        get_by (str): Optional. If provided, retrieves a specific user by email or ID

    Returns:
        JSON Response: A serialized list of user information in the response body
    """

    def get(self, request, get_by=None):
        """
        Handle GET requests for retrieving user information

        Parameters:
            request (Request): The HTTP request object
            get_by (str): Optional. If provided, retrieves a specific user by email or ID

        Returns:
            Response: A JSON response containing serialized user information
        """

        if get_by:
            users = CustomUser.objects.filter(Q(email__iexact=get_by) | Q(id__iexact=get_by))

        else:
            users = CustomUser.objects.all()

        serialized_user = UserSerializers(users, many=True)
        return Response(serialized_user.data)


class UsersExams(APIView):
    """
    API view to retrieve exams data for non-superuser

    Endpoint:
        GET api/users_exams/: Retrieve a list of all users containing email, FirstName, ProfileImage, TestsTaken

    Parameters:
        request: The HTTP request object

    Returns:
        Response: A serialized response containing email, FirstName, ProfileImage, TestsTaken for non-superuser
    """

    def get(self, request):
        """
        Retrieves and serializes exams data for non-superuser

        Parameters:
            request: The HTTP request object

        Returns:
            Response: A serialized response containing exams data for non-superuser
        """

        users = CustomUser.objects.filter(is_superuser=False)

        serialized_exams = UsersExamsSerializers(users, many=True)
        return Response(serialized_exams.data)


class UsersExamsInEachProgramme(APIView):
    """
    API View for retrieving exam details for a user

    Endpoint:
        GET api/users_exams_each_programmes/<user-email>: Retrieve a list of all exams or a specific exam by email

    Parameters:
        get_by (str): Optional. If provided, retrieves a specific exam by email

    Returns:
        JSON Response: A serialized list of exam information in the response body
    """

    def get(self, request, user_email):
        """
        Handle GET requests to retrieve exam details for a user

        Parameters:
            request (Request): Django request object containing the user email

        Returns:
            Response: Django Response object containing serialized exam details
        """

        resultExtraDetails = ResultsExtraDetails.objects.filter(UserID__email__iexact=user_email)
        serialized_resultExtraDetails = UsersExamsInEachProgrammeSerializers(resultExtraDetails, many=True)

        return Response(serialized_resultExtraDetails.data)


class Exam(APIView):
    """
    API View for retrieving exam information

    Endpoint:
        GET api/exams/<user_email>/<programme>: Retrieve a list of all exams or a specific exam by ID, Programme Name, or User Email

    Parameters:
        get_by (str): Optional. If provided, retrieves a specific exam by ID, Programme Name, or User Email

    Returns:
        JSON Response: A serialized list of exam information in the response body
    """

    def get(self, request, user_email, programme):
        """
        Handle GET requests for retrieving exam information

        Parameters:
            request (Request): The HTTP request object
            get_by (str): Optional. If provided, retrieves a specific exam by ID, Programme Name, or User Email

        Returns:
            Response: A JSON response containing serialized exam information
        """

        exams = Exams.objects.filter(Q(UserID__email__iexact=user_email) & Q(ProgrammeName__iexact=programme))
        serialized_exams = ExamSerializers(exams, many=True)
        return Response(serialized_exams.data)


class Programmes(APIView):
    """
    API View for retrieving programme information

    Endpoint:
        GET /programmes/: Retrieve a list of all programmes or a specific programme by ID or Name

    Parameters:
        get_by (str): Optional. If provided, retrieves a specific programme by ID or Name

    Returns:
        JSON Response: A serialized list of programme information in the response body
    """

    def get(self, request, get_by=None):
        """
        Handle GET requests for retrieving programme information

        Parameters:
            request (Request): The HTTP request object
            get_by (str): Optional. If provided, retrieves a specific programme by ID or Name

        Returns:
            Response: A JSON response containing serialized programme information
        """

        if get_by:
            programmes = Programme.objects.filter(Q(ID__iexact=get_by) | Q(Name__iexact=get_by))

        else:
            programmes = Programme.objects.all()

        serialized_programmes = ProgrammeSerializers(programmes, many=True)
        return Response(serialized_programmes.data)


class SubjectProgrammes(APIView):
    """
    API View for retrieving subject information

    Endpoint:
        GET api/subject-programmes/: Retrieve a list of all subject programmes list

    Returns:
        JSON Response: A serialized list of subject information in the response body
    """

    def get(self, request):
        """
        Handle GET requests for retrieving subject information

        Parameters:
            request (Request): The HTTP request object

        Returns:
            Response: A JSON response containing serialized subject information
        """

        subject_programmes = Programme.objects.all()
        serialized_subjects = SubjectProgrammesSerializers(subject_programmes, many=True)

        return Response(serialized_subjects.data)


class Subjects(APIView):
    """
    API View for retrieving subject information

    Endpoint:
        GET api/subjects/: Retrieve a list of all subjects or a specific subject by ID, Program Name, or Subject Name

    Parameters:
        get_by (str): Optional. If provided, retrieves a specific subject by ID, Program Name, or Subject Name

    Returns:
        JSON Response: A serialized list of subject information in the response body
    """

    def get(self, request, programme, subject=None):
        """
        Handle GET requests for retrieving subject information

        Parameters:
            request (Request): The HTTP request object
            subject (str): Optional. If provided, retrieves a specific subject Subject Name
            programme (str): Optional. If provided, retrieves a specific subject programme Name

        Returns:
            Response: A JSON response containing serialized subject information
        """

        if subject:
            subjects = Subject.objects.filter(ProgrammeID__Name__iexact=programme, Name__iexact=subject)

        else:
            subjects = Subject.objects.filter(ProgrammeID__Name__iexact=programme)

        serialized_subjects = SubjectProgrammeSerializers(subjects, many=True)
        return Response(serialized_subjects.data)


class QuestionProgrammes(APIView):
    """
    API View for retrieving question information

    Endpoint:
        GET api/questions/: Retrieve a list of all questions or specific questions by ID, SubjectID, Subject Name, or Title

    Parameters:
        get_by (str): Optional. If provided, retrieves specific questions by ID, SubjectID, Subject Name, or Title

    Returns:
        JSON Response: A serialized list of question information in the response body
    """

    def get(self, request):
        """
        Handle GET requests for retrieving question information

        Parameters:
        - request (Request): The HTTP request object
        - get_by (str): Optional. If provided, retrieves specific questions by ID, SubjectID, Subject Name, or Title

        Returns:
        - Response: A JSON response containing serialized question information
        """

        questions_progammes = Programme.objects.all()

        serialized_questions = QuestionProgrammesSerializers(questions_progammes, many=True)
        return Response(serialized_questions.data)


class QuestionProgrammeSubjects(APIView):
    """
    API View for retrieving question information

    Endpoint:
        GET api/questions/<progamme_name>: Retrieve a list of all questions or specific questions by ID, SubjectID, Subject Name, or Title

    Parameters:
        progamme_name (str): Optional. If provided, retrieves specific questions by ID, SubjectID, Subject Name, or Title

    Returns:
        JSON Response: A serialized list of question information in the response body
    """

    def get(self, request, progamme_name):
        """
        Handle GET requests for retrieving question information

        Parameters:
        - request (Request): The HTTP request object
        - progamme_name (str): Optional. If provided, retrieves specific questions by ID, SubjectID, Subject Name, or Title

        Returns:
        - Response: A JSON response containing serialized question information
        """

        questions_progammes_subjects = Subject.objects.filter(ProgrammeID__Name__iexact=progamme_name)

        serialized_questions = QuestionProgrammesSubjectsSerializers(questions_progammes_subjects, many=True)
        return Response(serialized_questions.data)


class QuestionPerSubject(APIView):
    """
    API View for retrieving question information

    Endpoint:
        GET api/questions/<programme>/<subject>: Retrieve a list of all questions or specific questions by ID, SubjectID, Subject Name, or Title

    Parameters:
        get_by (str): Optional. If provided, retrieves specific questions by ID, SubjectID, Subject Name, or Title

    Returns:
        JSON Response: A serialized list of question information in the response body
    """

    def get(self, request, programme, subject):
        """
        Handle GET requests for retrieving question information

        Parameters:
        - request (Request): The HTTP request object
        - get_by (str): Optional. If provided, retrieves specific questions by ID, SubjectID, Subject Name, or Title

        Returns:
        - Response: A JSON response containing serialized question information
        """

        questions_per_subjects = Questions.objects.filter(Q(SubjectID__ProgrammeID__Name__iexact=programme) & Q(SubjectID__Name__iexact=subject))

        serialized_questions = QuestionSerializers(questions_per_subjects, many=True)
        return Response(serialized_questions.data)


class Reports(APIView):
    """
    API View for retrieving reports information

    Endpoint:
        GET api/reports/: Retrieve a list of all reports or a specific report by ID

    Parameters:
        get_by (str): Optional. If provided, retrieves a specific report by ID

    Returns:
        JSON Response: A serialized list of report information in the response body
    """

    def get(self, request, get_by=None):
        """
        Handle GET requests for retrieving report information

        Parameters:
            request (Request): The HTTP request object
            get_by (str): Optional. If provided, retrieves a specific report by ID

        Returns:
            Response: A JSON response containing serialized report information
        """

        if get_by:
            reports = ReportQuestion.objects.filter(Q(ID__iexact=get_by) | Q(UserID__email__iexact=get_by) | Q(QuestionID__ID__iexact=get_by) | Q(QuestionID__Title__iexact=get_by))

        else:
            reports = ReportQuestion.objects.all()

        serialized_reports = ReportSerializers(reports, many=True)
        return Response(serialized_reports.data)


class Feedbacks(APIView):
    """
    API View for retrieving feedback information

    Endpoint:
        GET api/feedbacks/: Retrieve a list of all feedbacks

    Parameters:
        request (Request): The HTTP request object

    Returns:
        JSON Response: A serialized list of feedback information in the response body
    """

    def get(self, request):
        """
        Handle GET requests for retrieving feedback information

        Parameters:
            request (Request): The HTTP request object

        Returns:
            Response: A JSON response containing serialized feedback information
        """

        feedbacks = FeedBack.objects.all()

        serialized_feedbacks = FeedbackSerializers(feedbacks, many=True)
        return Response(serialized_feedbacks.data)


class Histories(APIView):
    """
    API View for retrieving history information

    Endpoint:
    - GET api/histories/: Retrieve history information based on the specified criteria

    Parameters:
        request (Request): The HTTP request object
        get_by (str): The criteria for retrieving history information

    Returns:
        Response: A JSON response containing serialized history information
    """

    def get(self, request, get_by):
        """
        Handle GET requests for retrieving history information

        Parameters:
            request (Request): The HTTP request object
            get_by (str): The criteria for retrieving history information

        Returns:
            Response: A JSON response containing serialized history information
        """

        histories = Exams.objects.filter(Q(UserID__id__iexact=get_by) | Q(UserID__email__iexact=get_by))

        serialized_histories = HistorySerializers(histories, many=True)

        return Response(serialized_histories.data)
