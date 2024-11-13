from django.db import models
from enumfields import EnumField

from src.tasks.utils import TaskStatusChoices


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='task_creator')
    deadline = models.PositiveSmallIntegerField(help_text='Время предполагаемого окончания')

    def __str__(self):
        return self.title


class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='statuses')
    status = EnumField(TaskStatusChoices, max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='status_responsible')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.task} - {self.status}"
