import datetime
from .models import Programme, Subject, Questions, CustomUser, Exams, ResultDetails, ReportQuestion, FeedBack


class UserFilter:
    """
    Utility class for filtering users based on various criteria.
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByEmail(self):
        """
        Filter users by email.

        Returns:
            List: A list of users matching the specified email.
        """

        return CustomUser.objects.filter(email=self.searching_value)

    def SearchByDOB(self):
        """
        Filter users by date of birth.

        Returns:
            List: A list of users matching the specified date of birth.
        """

        users = []
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for user in CustomUser.objects.all():
            dob = user.DOB

            if dob and dob == date:
                users.append(user)

        return users

    def SearchByGender(self):
        """
        Filter users by gender.

        Returns:
            List: A list of users matching the specified gender.
        """

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
        """
        Filter users by the date they became members.

        Returns:
            List: A list of users who became members on the specified date.
        """

        users = []
        memberSinceDate = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for user in CustomUser.objects.all():
            if memberSinceDate == user.MemberSince.date():
                users.append(user)

        return users

    def SearchByAdmin(self, is_admin=True):
        """
        Filter users by admin status.

        Parameters:
            is_admin (bool): If True, filter for admin users; if False, filter for non-admin users.

        Returns:
            List: A list of users matching the specified admin status.
        """

        return CustomUser.objects.filter(is_superuser=is_admin)

    def SearchByActive(self, is_active=True):
        """
        Filter users by active status.

        Parameters:
            is_active (bool): If True, filter for active users; if False, filter for inactive users.

        Returns:
            List: A list of users matching the specified active status.
        """

        return CustomUser.objects.filter(is_active=is_active)


class ExamFilter:
    """
    Utility class for filtering exams based on various criteria.
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByUser(self):
        """
        Filter exams by user.

        Returns:
            List: A list of exams taken by the specified user.
        """

        user = CustomUser.objects.filter(email=self.searching_value).first()

        if user:
            return Exams.objects.filter(UserID=user.id)

        return []

    def SearchByProgrammeName(self):
        """
        Filter exams by programme name.

        Returns:
            List: A list of exams matching the specified programme name.
        """

        return Exams.objects.filter(ProgrammeName=self.searching_value)

    def SearchByTotalCorrectAnswer(self):
        """
        Filter exams by the total number of correct answers.

        Returns:
            List: A list of exams with the specified total number of correct answers.
        """

        return Exams.objects.filter(CorrectCounter=self.searching_value)

    def SearchByDate(self):
        """
        Filter exams by date.

        Returns:
            List: A list of exams taken on the specified date.
        """

        programmes = []
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for detail in Exams.objects.all():
            if detail.Date == date:
                programmes.append(detail)

        return programmes


class SubjectFilter:
    """
    Utility class for filtering subjects based on various criteria.
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByProgrammeName(self):
        """
        Filter subjects by program name.

        Returns:
            List: A list of subjects matching the specified program name.
        """

        programmeID = Programme.objects.filter(Name=self.searching_value).first()

        return Subject.objects.filter(ProgrammeID=programmeID)

    def SearchBySubjectName(self):
        """
        Filter subjects by subject name.

        Returns:
            List: A list of subjects matching the specified subject name.
        """

        data = []
        subjects = Subject.objects.all()
        sub = self.searching_value.lower()

        for subject in subjects:
            subject_name = subject.Name.lower()

            if sub in subject_name:
                data.append(subject)

        return data

    def SearchByTotalQuestionsToSelect(self):
        """
        Filter subjects by the total number of questions to select.

        Returns:
            List: A list of subjects matching the specified total number of questions to select.
        """

        return Subject.objects.filter(TotalQuestionsToSelect=self.searching_value)


class QuestionFilter:
    """
    Utility class for filtering questions based on various criteria.
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchBySubject(self):
        """
        Filter questions by subject.

        Returns:
            List: A list of questions matching the specified subject.
        """

        questions = []

        for question in Questions.objects.all():
            subject = question.SubjectID.Name.lower()

            if subject == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByProgramme(self):
        """
        Filter questions by programme.

        Returns:
            List: A list of questions matching the specified programme.
        """

        questions = []

        for question in Questions.objects.all():
            programme = question.SubjectID.ProgrammeID.Name.lower()

            if programme == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByTitle(self):
        """
        Filter questions by title.

        Returns:
            List: A list of questions matching the specified title.
        """

        questions = []

        for question in Questions.objects.all():
            ques = question.Title.lower()

            if ques == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByAnswer(self):
        """
        Filter questions by answer.

        Returns:
            List: A list of questions matching the specified answer.
        """

        questions = []

        for question in Questions.objects.all():
            ans = question.Answer.lower()

            if ans == self.searching_value.lower():
                questions.append(question)

        return questions

    def SearchByOptions(self):
        """
        Filter questions by options.

        Returns:
            List: A list of questions matching the specified options.
        """

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
    """
    Utility class for filtering reports based on various criteria.
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByUser(self):
        """
        Filter reports by user.

        Returns:
            List: A list of reports related to the specified user.
        """

        user = CustomUser.objects.filter(email=self.searching_value).first()
        user = ReportQuestion.objects.filter(UserID=user).first()

        if user:
            return user

        return []

    def SearchByQuestion(self):
        """
        Filter reports by question.

        Returns:
            List: A list of reports related to the specified question.
        """

        issues = []

        for issue in ReportQuestion.objects.all():
            if issue.QuestionID.Title.lower().strip() == self.searching_value.lower().strip():
                issues.append(issue)

        return issues

    def SearchByIssue(self):
        """
        Filter reports by issue.

        Returns:
            List: A list of reports related to the specified issue.
        """

        issues = []

        for issue in ReportQuestion.objects.all():
            if self.searching_value.lower() == issue.Issue.lower():
                issues.append(issue)

        return issues

    def SearchByDate(self):
        """
        Filter reports by date.

        Returns:
            List: A list of reports related to the specified date.
        """

        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        return ReportQuestion.objects.filter(Date=date)

    def SearchByMarked(self, is_marked=True):
        """
        Filter reports by marked status.

        Parameters:
            is_marked (bool): If True, filter for marked reports; if False, filter for unmarked reports.

        Returns:
            List: A list of reports matching the specified marked status.
        """

        return ReportQuestion.objects.filter(IsMarked=is_marked)


class FeedbackFilter:
    """
    Utility class for filtering feedback based on various criteria.
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByName(self):
        """
        Filter feedback by name.

        Returns:
            List: A list of feedback matching the specified name.
        """

        feedbacks = []

        for feedback in FeedBack.objects.all():
            if self.searching_value.lower() == feedback.Name.lower():
                feedbacks.append(feedback)

        return feedbacks

    def SearchByEmail(self):
        """
        Filter feedback by email.

        Returns:
            List: A list of feedback matching the specified email.
        """

        return FeedBack.objects.filter(Email=self.searching_value)

    def SearchByMessage(self):
        """
        Filter feedback by message content.

        Returns:
            List: A list of feedback matching the specified message content.
        """

        feedbacks = []

        for feedback in FeedBack.objects.all():
            if self.searching_value.lower() == feedback.Message.lower():
                feedbacks.append(feedback)

        return feedbacks

    def SearchByMarked(self, is_marked=True):
        """
        Filter feedback by marked status.

        Parameters:
            is_marked (bool): If True, filter for marked feedback; if False, filter for unmarked feedback.

        Returns:
            List: A list of feedback matching the specified marked status.
        """

        return FeedBack.objects.filter(IsMarked=is_marked)

    def SearchByDate(self):
        """
        Filter feedback by date.

        Returns:
            List: A list of feedback matching the specified date.
        """

        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        return FeedBack.objects.filter(Date=date)
