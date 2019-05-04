from django.urls import path

from . import views


urlpatterns = [
    path('', views.index ,name='index'),
   	#path('sample/',views.indexx,name='indexx')
    path('details',views.algo,name='algo')
   
]
