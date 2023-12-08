from django.core.management.base import BaseCommand
from Users.models import *


class PopulateResultsExtraDetails:
    def Action(self):
        # Add required fields dynamically in ResultsExtraDetails Table
        fields = [programme.Name for programme in Programme.objects.all()]

        users = CustomUser.objects.filter(is_superuser=False)

        for RED in ResultsExtraDetails.objects.all():
            RED.delete()

        for user in users:
            arguments = dict()
            exams = Exams.objects.filter(UserID=user)

            for field in fields:
                arguments.update({
                    field.upper(): exams.filter(ProgrammeName=field).count()
                })

            arguments['UserID'] = user
            arguments['TestsTaken'] = exams.count()

            resultExtraDetails = ResultsExtraDetails(**arguments)
            resultExtraDetails.save()


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        PopulateResultsExtraDetails().Action()

    def handle(self, *args, **options):
        self._create_tags()
