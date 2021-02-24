from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('login',views.showLogin),
    path('register', views.showRegister),
    path('registerButton', views.register),
    path('loginButton', views.login),
    path('logout', views.logout),
    path('dashboard/admin', views.showDashboard),
    path('dashboard/admin/add/', views.showAddActivity),
    path('activities/create', views.createActivity),
    path('activities', views.showActivities),
    path('activity/<int:activity_id>', views.showActivity),
    path('activities/filter', views.activitiesFilter),
    path('dashboard/admin/edit/<int:activity_id>', views.editActivity),
    path('dashboard/admin/save/<int:activity_id>', views.saveActivity),
    path('dashboard/admin/destroy/<int:activity_id>', views.deleteActivity),
    path('comment/create/<int:activity_id>', views.createComment)


    ]