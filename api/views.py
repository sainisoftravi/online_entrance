from Users.models import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class Users(APIView):
    def get(self, request, get_by=None):
        if get_by:
            users = CustomUser.objects.filter(Q(email__iexact=get_by) | Q(id__iexact=get_by))

        else:
            users = CustomUser.objects.all()

        serialized_user = UserSerializers(users, many=True)
        return Response(serialized_user.data)

    def post(self, request):
        pass


class Exam(APIView):
    def get(self, request, get_by=None):
        if get_by:
            exams = Exams.objects.filter(Q(ID__iexact=get_by) | Q(ProgrammeName__iexact=get_by) | Q(UserID__email__iexact=get_by))

        else:
            exams = Exams.objects.all()

        serialized_exams = ExamSerializers(exams, many=True)
        return Response(serialized_exams.data)

    def post(self, request):
        pass


class Programmes(APIView):
    def get(self, request, get_by=None):
        if get_by:
            programmes = Programme.objects.filter(Q(ID__iexact=get_by) | Q(Name__iexact=get_by))

        else:
            programmes = Programme.objects.all()

        serialized_programmes = ProgrammeSerializers(programmes, many=True)
        return Response(serialized_programmes.data)

    def post(self, request):
        pass


class Subjects(APIView):
    def get(self, request, get_by=None):
        if get_by:
            subjects = Subject.objects.filter(Q(ID__iexact=get_by) | Q(ProgrammeID__Name__iexact=get_by) | Q(Name__iexact=get_by))

        else:
            subjects = Subject.objects.all()

        serialized_subjects = SubjectSerializers(subjects, many=True)
        return Response(serialized_subjects.data)

    def post(self, request):
        pass


class Question(APIView):
    def get(self, request, get_by=None):
        if get_by:
            questions = Questions.objects.filter(Q(ID__iexact=get_by) | Q(SubjectID__Name__iexact=get_by) | Q(SubjectID__ProgrammeID__Name__iexact=get_by) | Q(Title__iexact=get_by))

        else:
            questions = Questions.objects.all()

        serialized_questions = QuestionSerializers(questions, many=True)
        return Response(serialized_questions.data)

    def post(self, request):
        pass


class Reports(APIView):
    def get(self, request, get_by=None):
        if get_by:
            reports = ReportQuestion.objects.filter(Q(ID__iexact=get_by) | Q(UserID__email__iexact=get_by) | Q(QuestionID__ID__iexact=get_by) | Q(QuestionID__Title__iexact=get_by))

        else:
            reports = ReportQuestion.objects.all()

        serialized_reports = ReportSerializers(reports, many=True)
        return Response(serialized_reports.data)

    def post(self, request):
        pass


class Feedbacks(APIView):
    def get(self, request):
        feedbacks = FeedBack.objects.all()

        serialized_feedbacks = FeedbackSerializers(feedbacks, many=True)
        return Response(serialized_feedbacks.data)
