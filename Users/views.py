from django.shortcuts import render
from django.http import HttpResponse


def Eg(request):
    text = ''' \\(\\frac{(n+1)^{2}}{2}\\)'''
    value = {'value': text}
    return render(request, 'Users/Signup.html', value)

