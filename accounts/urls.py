from django.urls import include, path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logging/', views.logging, name='logging'),
    path('logout/', views.logoutView, name='logout')
]
