from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]