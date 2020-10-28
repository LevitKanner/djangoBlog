from django.shortcuts import render
from .models import Personal

# Create your views here.
def index(request):
    info = Personal.objects.all()[0]
    languages = info.languages.all()
    return render(request, 'portfolio/index.html', {'info': info, 'languages': languages})