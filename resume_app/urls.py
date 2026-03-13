from django.urls import path
from . import views  # ← Import views module

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('delete/<int:pk>/', views.delete_resume, name='delete_resume'),  # Now views.delete_resume exists
]
