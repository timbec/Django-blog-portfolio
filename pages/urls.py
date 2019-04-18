from django.urls import path, include

from . import views

from .views import contact, successView

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('success/', successView, name='success'),

]
