from django.contrib import admin
from django.urls import path

from . import views

app_name = 'watsons'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail', views.RFM_model, name='RFM'),
    path('RFM_list', views.RFM_model_list, name='RFM_list'),
    path('RFM_group', views.RFM_model_group, name='RFM_group'),
    path('product_index', views.product_index, name='Product Index'),  
    path('listall', views.listall, name='List all'),
    path('create', views.create, name='create'),
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    path('show_transaction', views.showTransaction, name='showTransaction'),
    path('home/servive/', views.servive, name='servive'),        #存活率
    path('home/total_rate/', views.total_rate, name='total_rate'),  #個別錢包佔有率
    path('home/rate/', views.rate, name='rate'), 
    path('home', views.home, name='home'),     
]