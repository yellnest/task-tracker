from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from src.tasks.views import RegisterView

urlpatterns = [
    # Основные
    path('', include('task_tracker.routers')),

    # JWT токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('token/register/', UserCreateView.as_view(), name='user_register'),

    # Регистрация
    path('reg/', RegisterView.as_view(), name='register'),
]
