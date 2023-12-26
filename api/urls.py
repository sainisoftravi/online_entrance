from django.urls import path
from . import views


urlpatterns = [
    path('api/users', views.Users.as_view()),
    path('api/reports', views.Reports.as_view()),
    path('api/subjects', views.Subjects.as_view()),
    path('api/feedbacks', views.Feedbacks.as_view()),
    path('api/programmes', views.Programmes.as_view()),
    path('api/users_exams', views.UsersExams.as_view()),
    path('api/users/<str:get_by>', views.Users.as_view()),
    path('api/questions', views.QuestionProgrammes.as_view()),
    path('api/reports/<str:get_by>', views.Reports.as_view()),
    path('api/subjects/<str:get_by>', views.Subjects.as_view()),
    path('api/histories/<str:get_by>', views.Histories.as_view()),
    path('api/programmes/<str:get_by>', views.Programmes.as_view()),
    path('api/exams/<str:user_email>/<str:programme>', views.Exam.as_view()),
    path('api/questions/<str:progamme_name>', views.QuestionProgrammeSubjects.as_view()),
    path('api/questions/<str:programme>/<str:subject>', views.QuestionPerSubject.as_view()),
    path('api/users_exams_each_programmes/<str:user_email>', views.UsersExamsInEachProgramme.as_view()),
]
