import os
import json
from pathlib import Path
from django.shortcuts import render


def SignUp(request):
    conditions = {
        'login': False
    }

    return render(request, 'Signup.html', conditions)


def Login(request):
    conditions = {
        'login': True
    }
    return render(request, 'Signup.html', conditions)


def Index(request):
    return render(request, 'index.html')


def TakeModelTest(request):
    questions = dict()

    BASE_DIR = Path(__file__).resolve().parent.parent
    jsonPath = os.path.join(BASE_DIR, 'static', 'Questions.json')

    with open(jsonPath) as f:
        contents = json.load(f)

    # all_contents = contents['BCA']['English']
    # all_contents.update(contents['BCA']['Math'])

    # for i in range(200):
    #     all_keys = list(all_contents.keys())
    #     question = random.choice(all_keys)

    #     questions[question] = all_contents[question]['choices']
    #     all_contents.pop(question)

    all_contents = contents['BCA']['Math']

    for question, values in all_contents.items():
        questions[question] = values['choices']

    values = {
        'nums': list(range(100)),
        'questions': questions
    }

    return render(request, 'ModelTest.html', values)
