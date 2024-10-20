# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_page, name='upload_page'),  # Upload form at root
    path('predict/', views.predict_image, name='predict_image'),  # Prediction URL
    path('solution/', views.SolutionView, name='solution'),
    path("signup/", views.signup_view, name="signup"),  # Signup view
    path("home/", views.login_view, name="login"),  # Login view (no leading slash)
    path("", views.logout_view, name="logout"),
    path("community/", views.CommunityView, name="community"),
    path('remove/<int:id>/', views.remove, name='delete'),
    
]
