from Users.models import *
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'DOB', 'ProfileImage', 'MemberSince', 'Gender', 'is_superuser', 'is_active']


class ExamSerializers(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Exams
        fields = ['ID', 'Slug', 'user_email', 'ProgrammeName', 'CorrectCounter', 'Date', 'UserID']

    def get_user_email(self, obj):
        return obj.UserID.email


class ProgrammeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = '__all__'


class SubjectSerializers(serializers.ModelSerializer):
    programme_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_programme_name(self, obj):
        return obj.ProgrammeID.Name


class QuestionSerializers(serializers.ModelSerializer):
    Options = serializers.SerializerMethodField()
    Subject = serializers.SerializerMethodField()
    Programme = serializers.SerializerMethodField()

    class Meta:
        model = Questions
        fields = ['ID', 'Title', 'Answer', 'Subject', 'Programme', 'Options']

    def get_Programme(self, obj):
        return obj.SubjectID.ProgrammeID.Name

    def get_Subject(self, obj):
        return obj.SubjectID.Name

    def get_Options(self, obj):
        return [obj.OptionOne, obj.OptionTwo, obj.OptionThree, obj.OptionFour]


class ReportSerializers(serializers.ModelSerializer):
    User = serializers.SerializerMethodField()
    Date = serializers.SerializerMethodField()
    Question = serializers.SerializerMethodField()

    class Meta:
        model = ReportQuestion
        fields = ['ID', 'User', 'Issue', 'Question', 'Date', 'IsMarked', 'QuestionID']

    def get_User(self, obj):
        return obj.UserID.email

    def get_Date(self, obj):
        return datetime.datetime.strptime(str(obj.Date), '%Y-%m-%d').strftime('%b %d, %Y')

    def get_Question(self, obj):
        return obj.QuestionID.Title


class FeedbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['ID', 'Name', 'Email', 'Message', 'Date']
