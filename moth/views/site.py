from django.shortcuts import render


def home(request):
    return render(request, 'moth/home.html')

def about(request):
    return render(request, 'moth/about.html')
