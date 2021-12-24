from django.urls import path
from jobboard.views import board

urlpatterns = [
    path('', board, name='board'),
]
