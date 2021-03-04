from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_friends),
    path('add/<int:num>', views.add_friend),
    path('del_friend/<int:num>', views.remove_friend),
    path('<int:num>/', views.show_user),
]