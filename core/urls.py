from django.urls import path
from .views import RegisterView, LoginView, LogoutView, get_user_details

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-user/', get_user_details, name='get-user'),
]
