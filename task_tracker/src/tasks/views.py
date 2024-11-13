from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_tracker.permission import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import Task, TaskStatus
from .serializers import TaskSerializer, UserSerializer, RegisterSerializer
from .utils import TaskStatusChoices


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(created_by=self.request.user)

    @staticmethod
    def _create_task_status(instance, status, responsible_id):
        query = TaskStatus.objects.filter(task=instance, status=status)
        if query.exists():
            # raise serializers.ValidationError('Task status already exists')
            return query.update(responsible_id=responsible_id)
        TaskStatus.objects.create(task=instance, status=status, responsible_id=responsible_id, date=timezone.now())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        self._create_task_status(serializer.instance, TaskStatusChoices.CREATED, self.request.user.id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Логика добавления статусов при изменении исполнителя
        if 'assigned_to' in request.data:
            self._create_task_status(instance, TaskStatusChoices.ASSIGNED, request.data['assigned_to'])

        if 'completed_by' in request.data:
            self._create_task_status(instance, TaskStatusChoices.COMPLETED, request.data['completed_by'])

        if 'checked_by' in request.data:
            self._create_task_status(instance, TaskStatusChoices.CHECKED, request.data['checked_by'])

        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]


class RegisterView(generics.GenericAPIView):
    """Регистрация пользователя
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан'
        })
