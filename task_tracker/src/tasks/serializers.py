from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers
from .models import Task, TaskStatus
from django.contrib.auth.models import User


class TaskStatusSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ('status', 'date', 'responsible')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['responsible'] = instance.responsible.username
        return rep


class TaskSerializer(serializers.ModelSerializer):
    statuses = TaskStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'created_by', 'deadline', 'statuses')
        extra_kwargs = {
            'created_by': {'read_only': True},
            'statuses': {'read_only': True}
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_by'] = instance.created_by.username
        return rep


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
