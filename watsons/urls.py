from django.contrib import admin
from django.urls import path

from . import views

app_name = 'watsons'

urlpatterns = [
    path('', views.index, name='index'),
    path('product_index', views.product_index, name='Product Index'),  
    path('RFM/chart', views.RFM_model, name='RFM'),
    path('RFM/list', views.RFM_model_list, name='RFM_list'),
    path('RFM/group', views.RFM_model_group, name='RFM_group'),
    path('breakeven/list', views.BreakEven, name='BreakEven'),
    path('breakeven/edit', views.get_promotion, name='edit_BreakEven'),
    # path('association', views.Association_Rule, name='Association'),
    path('listall', views.listall, name='List all'),
    path('listone', views.listone, name='List one'),
    path('listless', views.listless, name='List less'),
    path('create', views.create, name='create'),
    path('show_transaction', views.showTransaction, name='showTransaction'),
    # path('transaction/upload', views.uploadTransaction, name='uploadTransaction'),
    # path('file', views.readFile, name='readFile'),
    # path('transaction/import', views.importTransaction, name='importTransaction'),
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    path('home/servive/', views.servive, name='servive'),        #存活率
    path('home/total_rate/', views.total_rate, name='total_rate'),  #個別錢包佔有率
    path('home/rate/', views.rate, name='rate'), 
]