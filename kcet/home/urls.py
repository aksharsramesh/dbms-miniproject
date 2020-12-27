from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='kcet-home'),
    path('about/', views.about, name='kcet-about'),
]