from django.urls import path, include

from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.show, name='show'),
    path('data/<int:id>', views.data, name='data'),
    path('auth', views.auth, name='auth'),
]
