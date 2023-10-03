from django.shortcuts import render


def get_access(request):
    return render(request, 'registration.html')
