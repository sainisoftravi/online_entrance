from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('login/', views.Login, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('getresult/', views.GetResult, name='getresult'),
    path('deleteaccount/', views.DeleteAccount, name='deleteaccount'),
    path('updateprofile/', views.UpdateProfile, name='updateprofile'),
    path('modeltest/<program>', views.TakeModelTest, name='modeltest'),
    path('updatepassword/', views.UpdatePassword, name='updatepassword'),
    path('programselector/', views.ProgramSelector, name='programselector'),
    path('detailed-result/<slug:slug>', views.DetailedHistory, name='detailed-history'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='FindAccount.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetView.as_view(template_name='ResetPasswordSent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='NewPassword.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='RecoverPasswordComplete.html'), name='password_reset_complete'),
    path('<str:redirect_to>/', views.GoTo, name='go_to'),
]
