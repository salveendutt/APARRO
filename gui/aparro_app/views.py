from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')

def ready_page(request):
    return render(request, 'ready_page.html')