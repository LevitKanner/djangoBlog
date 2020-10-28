from . import views
from django.urls import path

app_name = 'portfolio'

urlpatterns = [
    path('', views.index, name='portfolio_index' )
]