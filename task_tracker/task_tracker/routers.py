from rest_framework.routers import DefaultRouter

from src.tasks.views import TaskViewSet, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')  # Specify basename here
router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls
