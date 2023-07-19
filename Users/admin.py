# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Programme, Subject, Questions, Results, ResultDetails, FeedBack


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password', 'ProfileImage')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'password', 'DOB', 'Gender', 'ProfileImage', 'MemberSince', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('ID', 'ProgrammeID', 'Name')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'SubjectID', 'Title', 'Answer', 'OptionOne', 'OptionTwo', 'OptionThree', 'OptionFour')


class ResultsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'UserID', 'ProgrammeName', 'CorrectCounter', 'Date')


class ResultsDetailsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'ResultID', 'QuestionID', 'UserAnswer')


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Email')


admin.site.register(Results, ResultsAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(FeedBack, FeedBackAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(ResultDetails, ResultsDetailsAdmin)
