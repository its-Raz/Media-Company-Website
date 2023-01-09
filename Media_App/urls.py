from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
path('index',views.index, name='index'),
    path('Query', views.Query, name='Query'),
path('Rankings', views.Rankings, name='Rankings'),
path('Records', views.Records, name='Records'),
path('addNewRank', views.addNewRank, name='addNewMovie'),
path('submitNumber', views.submitNumber, name='submitNumber')


]