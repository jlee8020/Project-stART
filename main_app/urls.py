from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('art/', views.art_index, name='art_index'),
    path('art/create', views.ArtCreate.as_view(), name='art_create'),
    path('art/<int:art_id>/', views.art_detail, name='art_detail'),
    path('art/<int:art_id>/add_photo/', views.add_photo, name='add_photo'),
]
