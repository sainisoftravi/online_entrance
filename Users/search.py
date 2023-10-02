import datetime
from .models import Programme, Subject, Questions, CustomUser, Exams, ResultDetails, ReportQuestion, FeedBack


class UserFilter:
    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByEmail(self):
        return CustomUser.objects.filter(email=self.searching_value)

    def SearchByDOB(self):
        users = []
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for user in CustomUser.objects.all():
            dob = user.DOB

            if dob and dob == date:
                users.append(user)

        return users

    def SearchByGender(self):
        gender = self.searching_value.lower()

        maps = {
            'm': 'male',
            'f': 'female',
            'o': 'others'
        }

        gender = gender.lower()

        if gender in maps:
            gender = maps[gender]

        return CustomUser.objects.filter(Gender=gender)

    def SearchByMemberSince(self):
        users = []
        memberSinceDate = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for user in CustomUser.objects.all():
            if memberSinceDate == user.MemberSince.date():
                users.append(user)

        return users

    def SearchByAdmin(self, is_admin=True):
        return CustomUser.objects.filter(is_superuser=is_admin)

    def SearchByActive(self, is_active=True):
        return CustomUser.objects.filter(is_active=is_active)


class ExamFilter:
    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByUser(self):
        user = CustomUser.objects.filter(email=self.searching_value).first()

        if user:
            return Exams.objects.filter(UserID=user.id)

        return []

    def SearchByProgrammeName(self):
        return Exams.objects.filter(ProgrammeName=self.searching_value)

    def SearchByTotalCorrectAnswer(self):
        return Exams.objects.filter(CorrectCounter=self.searching_value)

    def SearchByDate(self):
        programmes = []
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for detail in Exams.objects.all():
            if detail.Date == date:
                programmes.append(detail)

        return programmes


class SubjectFilter:
    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByProgrammeName(self):
        programmeID = Programme.objects.filter(Name=self.searching_value).first()

        return Subject.objects.filter(ProgrammeID=programmeID)

    def SearchBySubjectName(self):
        data = []
        subjects = Subject.objects.all()
        sub = self.searching_value.lower()

        for subject in subjects:
            subject_name = subject.Name.lower()

            if sub in subject_name:
                data.append(subject)

        return data

    def SearchByTotalQuestionsToSelect(self):
        return Subject.objects.filter(TotalQuestionsToSelect=self.searching_value)


class QuestionFilter:
    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchBySubject(self):
        questions = []

        for question in Questions.objects.all():
            subject = question.SubjectID.Name.lower()

            if subject == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByProgramme(self):
        questions = []

        for question in Questions.objects.all():
            programme = question.SubjectID.ProgrammeID.Name.lower()

            if programme == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByTitle(self):
        questions = []

        for question in Questions.objects.all():
            ques = question.Title.lower()

            if ques == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByAnswer(self):
        questions = []

        for question in Questions.objects.all():
            ans = question.Answer.lower()

            if ans == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByOptions(self):
        questions = []

        for question in Questions.objects.all():
            optionOne = question.OptionOne.lower()
            optionTwo = question.OptionTwo.lower()
            optionFour = question.OptionFour.lower()
            optionThree = question.OptionThree.lower()

            options = [optionOne, optionTwo, optionThree, optionFour]

            if self.searching_value.lower() in options:
                questions.append(question)

        return questions


class ReportFilter:
    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByUser(self):
        user = CustomUser.objects.filter(email=self.searching_value).first()
        user = ReportQuestion.objects.filter(UserID=user).first()

        if user:
            return user

        return []

    def SearchByQuestion(self):
        issues = []

        for issue in ReportQuestion.objects.all():
            if issue.QuestionID.Title.lower().strip() == self.searching_value.lower().strip():
                issues.append(issue)

        return issues

    def SearchByIssue(self):
        issues = []

        for issue in ReportQuestion.objects.all():
            if self.searching_value.lower() == issue.Issue.lower():
                issues.append(issue)

        return issues

    def SearchByDate(self):
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        return ReportQuestion.objects.filter(Date=date)

    def SearchByMarked(self, is_marked=True):
        return ReportQuestion.objects.filter(IsMarked=is_marked)


class FeedbackFilter:
    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByName(self):
        feedbacks = []

        for feedback in FeedBack.objects.all():
            if self.searching_value.lower() == feedback.Name.lower():
                feedbacks.append(feedback)

        return feedbacks

    def SearchByEmail(self):
        return FeedBack.objects.filter(Email=self.searching_value)

    def SearchByMessage(self):
        feedbacks = []

        for feedback in FeedBack.objects.all():
            if self.searching_value.lower() == feedback.Message.lower():
                feedbacks.append(feedback)

        return feedbacks

    def SearchByMarked(self, is_marked=True):
        return FeedBack.objects.filter(IsMarked=is_marked)

    def SearchByDate(self):
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        return FeedBack.objects.filter(Date=date)
