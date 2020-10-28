from django.shortcuts import render
from .models import Personal
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    info = get_object_or_404(Personal, name='Levit Osei-Wusu')
    languages = info.languages.all()
    return render(request, 'portfolio/index.html', {'info': info, 'languages': languages})