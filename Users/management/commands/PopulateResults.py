import random
from django.core.management.base import BaseCommand
from Users.models import CustomUser, Programme, Subject, Questions, Results, ResultDetails


class PopulateResults:
    def __init__(self, Prog, Email, NumberOfResultsToGenerate):
        self.Email = Email
        self.Programme = Prog
        self.NumberOfResultsToGenerate = NumberOfResultsToGenerate

        self.ProgrammeObj = Programme.objects.filter(Name=self.Programme).first()
        self.UsersObj = CustomUser.objects.filter(email=self.Email).first()

    def GetSubjects(self):
        SubjectsID = []

        for id in Subject.objects.filter(ProgrammeID=self.ProgrammeObj):
            SubjectsID.append(id)

        return SubjectsID

    def Action(self):
        allSubjects = self.GetSubjects()

        for _ in range(self.NumberOfResultsToGenerate):
            correct_counter = 0

            results = Results(UserID=self.UsersObj, ProgrammeName=self.Programme)
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
        email = input("Enter user's email: ")
        programme = input("Enter programme: ")
        numberOfResults = int(input("Enter the number of results to generate: "))  # 40

        PopulateResults(programme, email, numberOfResults).Action()

    def handle(self, *args, **options):
        self._create_tags()
