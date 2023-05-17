from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('login/', views.Login, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('modeltest/', views.TakeModelTest, name='modeltest'),
]
