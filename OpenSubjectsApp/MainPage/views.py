from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello!")

def main_button(request):
    return render(request, 'MainPage/index.html')