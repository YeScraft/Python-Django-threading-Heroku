from django.shortcuts import render


def index(request):
    message = 'Это домашняя работа E 2.9.'
    return render(request, 'index.html', context={'message': message})

