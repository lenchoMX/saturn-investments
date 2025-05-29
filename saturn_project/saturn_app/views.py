from django.shortcuts import render

def index(request):
    return render(request, 'saturn_app/index.html', {'title': 'Saturn Investments'})
