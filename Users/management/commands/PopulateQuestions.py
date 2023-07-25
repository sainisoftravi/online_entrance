import json
from pathlib import Path
from django.core.management.base import BaseCommand
from Users.models import Programme, Subject, Questions


class PopulateQuestions:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        self.JSON_FILE = self.BASE_DIR / 'static' / 'Questions.json'

        with open(self.JSON_FILE, 'r') as f:
            self.Contents = json.load(f)

    def Action(self):
        for content in self.Contents:
            answer = content['answer']
            choices = content['choices']
            subject = content['subject']
            question = content['question']
            programme = content['programme']
            TotalQuestionsToSelect = content['TotalQuestionsToSelect']

            programmeObj = Programme.objects.filter(Name=programme)

            if programmeObj:
                programmeObj = programmeObj.first()

            else:
                programmeObj = Programme(Name=programme)
                programmeObj.save()

            subjectObj = Subject.objects.filter(ProgrammeID=programmeObj, Name=subject)

            if subjectObj:
                subjectObj = subjectObj.first()

            else:
                subjectObj = Subject(ProgrammeID=programmeObj, Name=subject)
                subjectObj.save()

            if subjectObj.TotalQuestionsToSelect == 1:
                subjectObj.TotalQuestionsToSelect = TotalQuestionsToSelect
                subjectObj.save()

            if not Questions.objects.filter(SubjectID=subjectObj, Title=question, Answer=answer):
                questionObj = Questions(
                                    SubjectID=subjectObj, Title=question, Answer=answer,
                                    OptionOne=choices[0], OptionTwo=choices[1],
                                    OptionThree=choices[2], OptionFour=choices[3]
                                )

                questionObj.save()


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        PopulateQuestions().Action()

    def handle(self, *args, **options):
        self._create_tags()
