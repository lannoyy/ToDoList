from django.urls import path
from account.auth import CustomAuthorizationView

urlpatterns = [
    path('sign_in', CustomAuthorizationView.as_view()),
]
