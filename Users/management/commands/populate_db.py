import json
from pathlib import Path
from django.core.management.base import BaseCommand
from Users.models import Programme, Subject, Questions


class SaveIntoDB:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        self.JSON_FILE = self.BASE_DIR / 'static' / 'Questions.json'

        with open(self.JSON_FILE, 'r') as f:
            self.Contents = json.load(f)

    def GetSubjects(self, programme):
        return list(self.Contents[programme].keys())

    def Action(self):
        for programme, _ in self.Contents.items():
            ProgramObj = Programme.objects.filter(Name=programme)

            if ProgramObj:
                ProgramObj = ProgramObj[0]

            else:
                ProgramObj = Programme(Name=programme)
                ProgramObj.save()

            subjects = self.GetSubjects(programme)

            for subject in subjects:
                SubjectObj = Subject.objects.filter(ProgrammeID=ProgramObj, Name=subject)

                if SubjectObj:
                    SubjectObj = SubjectObj[0]

                else:
                    SubjectObj = Subject(ProgrammeID=ProgramObj, Name=subject)
                    SubjectObj.save()

                for question, question_values in self.Contents[programme][subject].items():
                    if not Questions.objects.filter(SubjectID=SubjectObj, Title=question):
                        answer = question_values['answer']
                        choices = question_values['choices']

                        new_question = Questions(
                                            SubjectID=SubjectObj, Title=question, Answer=answer,
                                            OptionOne=choices[0], OptionTwo=choices[1],
                                            OptionThree=choices[2], OptionFour=choices[3]
                                        )

                        new_question.save()


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        SaveIntoDB().Action()

    def handle(self, *args, **options):
        self._create_tags()
