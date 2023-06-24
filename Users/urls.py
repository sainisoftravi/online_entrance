from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('login/', views.Login, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('getresult/', views.GetResult, name='getresult'),
    path('deleteaccount/', views.DeleteAccount, name='deleteaccount'),
    path('updateprofile/', views.UpdateProfile, name='updateprofile'),
    path('modeltest/<program>', views.TakeModelTest, name='modeltest'),
    path('updatepassword/', views.UpdatePassword, name='updatepassword'),
    path('programselector/', views.ProgramSelector, name='programselector'),
]
