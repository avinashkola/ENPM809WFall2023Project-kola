from django.urls import path
from . import views

app_name = 'chores'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:chore_id>/complete_chore/', views.complete_chore, name='complete_chore'),
    path('<int:chore_id>/delete_chore/', views.delete_chore, name='delete_chore'),
    path('create_chore/', views.create_chore, name='create_chore'),
]
