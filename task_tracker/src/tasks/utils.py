from enum import Enum


class TaskStatusChoices(Enum):
    CREATED = 'Задача создана'
    ASSIGNED = 'Назначен исполнитель'
    COMPLETED = 'Задача выполнена'
    CHECKED = 'Задача проверена'
