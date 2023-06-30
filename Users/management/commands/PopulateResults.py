import random
from django.core.management.base import BaseCommand
from Users.models import CustomUser, Programme, Subject, Questions, Results, ResultDetails


class PopulateResults:
    def __init__(self, Prog):
        self.Programme = Prog
        self.ProgrammeObj = Programme.objects.filter(Name=self.Programme)[0]
        self.UsersObj = CustomUser.objects.filter(email='ghanteyyy@gmail.com')[0]

    def GetSubjects(self):
        SubjectsID = []

        for id in Subject.objects.filter(ProgrammeID=self.ProgrammeObj):
            SubjectsID.append(id)

        return SubjectsID

    def Action(self):
        correct_counter = 0
        user_id = CustomUser.objects.filter(email='ghanteyyy@gmail.com')[0]

        allSubjects = self.GetSubjects()

        results = Results(UserID=user_id, ProgrammeName=self.Programme)
        results.save()

        for subject in allSubjects:
            total_questions_per_subject = subject.TotalQuestionsToSelect
            number_of_correct_answers_to_select = random.randint(1, total_questions_per_subject)

            correct_counter += number_of_correct_answers_to_select

            questions = list(Questions.objects.filter(SubjectID=subject.ID))
            random.shuffle(questions)

            for num in range(total_questions_per_subject):
                question = questions[num]
                wrong_or_right = random.SystemRandom().choice([0, 1])

                if number_of_correct_answers_to_select > 0 and wrong_or_right:
                    user_answer = question.Answer
                    number_of_correct_answers_to_select -= 1

                else:
                    choices = [question.OptionOne, question.OptionTwo, question.OptionThree, question.OptionFour]
                    choices = [choice for choice in choices if choice != question.Answer]
                    user_answer = random.choice(choices)

                result_details = ResultDetails(
                                    ResultID = results,
                                    QuestionID = question,
                                    UserAnswer = user_answer
                                )

                result_details.save()

            results.CorrectCounter = correct_counter
            results.save()


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        PopulateResults('BCA').Action()

    def handle(self, *args, **options):
        self._create_tags()
