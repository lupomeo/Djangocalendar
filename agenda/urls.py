from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('agenda', views.agenda, name='agenda'),
    path("createevent/", views.createevent, name="createevent"),
    path("getevents/", views.getevents, name="getevents"),
    path("editevent/", views.editevent, name="editevent"),
    path("deleteevent/", views.deleteevent, name="deleteevent"),
    path('profile/', views.profile, name='profile'),
    path('saveprofile/<int:id>', views.saveprofile, name='saveprofile'),
    path('users/', views.users, name='users'),
    path('jsonresponse/ausers', views.ausers, name='ausers'),
    path('storeuser', views.storeuser, name='storeuser'),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
]