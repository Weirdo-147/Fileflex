from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('history/', views.view_history, name='view_history'),
    path('convert/', views.convert_file, name='convert_file'),
    path('pricing/', views.subscription_plans, name='subscription_plans'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]