import os
import uuid
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
import requests
from Users.models import CustomUser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ImagePath = os.path.join(BASE_DIR, "static", "images", f"{uuid.uuid4().hex}.jpg")

class PopulateUsers:
    def __init__(self):
        pass

class Command(BaseCommand):
    def GetNumberOfUsers(self):
        while True:
            number_of_users = input("Enter number of users to create: ")

            if number_of_users.isdigit():
                return int(number_of_users)

            else:
                print('\nInvalid number of users. Try again\n')

    def CreateUsers(self):
        Random_Users_Lists = requests.get(f'https://randomuser.me/api/?results={self.number_of_users}').json()['results']

        for index, user_list in enumerate(Random_Users_Lists):
            email = user_list['email']

            print(f"Creating user ... {index + 1}/{len(Random_Users_Lists)}")

            if CustomUser.objects.filter(email=email):
                new_user = requests.get(f'https://randomuser.me/api/').json()['results'][0]
                Random_Users_Lists.append(new_user)

                continue

            gender = user_list['gender']
            dob = user_list['dob']['date'].split('T')[0]
            full_name = f'{user_list["name"]["first"]} {user_list["name"]["last"]}'

            with open(ImagePath, 'wb') as img:
                image = requests.get(user_list['picture']['large']).content
                img.write(image)

            contentfile = ContentFile(image)

            user = CustomUser(
                DOB = dob,
                email = email,
                Gender = gender,
                FullName = full_name,
            )

            user.set_password('root')
            user.ProfileImage.save(ImagePath, contentfile)
            user.save()

        os.remove(ImagePath)

    def _create_tags(self):
        self.number_of_users = self.GetNumberOfUsers()

        self.CreateUsers()

    def handle(self, *args, **options):
        self._create_tags()
