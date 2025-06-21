from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_poem, name='add_poem'),
    path('poem/<int:poem_id>/', views.poem_detail, name='poem_detail'),
    path('poem/<int:poem_id>/delete/', views.delete_poem, name='delete_poem'),
    path('unsafe_search/', views.unsafe_search, name='unsafe_search'),
 #   path('register/', views.register, name='register'), FLAW 2: A07:2021 - add this
]
