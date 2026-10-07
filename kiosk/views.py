from django.shortcuts import render


def home(request):
    """Present the visual foundation; no active transaction exists yet."""
    return render(request, 'kiosk/home.html')
