from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('art/', views.art_index, name='art_index'),
    path('art/create', views.ArtCreate.as_view(), name='art_create'),
    path('art/<int:art_id>/', views.art_detail, name='art_detail'),
    path('art/<int:art_id>/add_photo/', views.add_photo, name='add_photo'),
    path('art/<int:art_id>/delete_photo/', views.delete_photo, name='delete_photo'),
    path('art/<int:art_id>/add_comment/', views.add_comment, name='add_comment'),

    path('art/<int:pk>/update/', views.ArtUpdate.as_view(), name='art_update'),    
    path('art/<int:pk>/delete/', views.ArtDelete.as_view(), name='art_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    
]
