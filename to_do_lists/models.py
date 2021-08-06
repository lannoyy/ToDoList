from django.db import models
from organisation.models import Organisation


class ToDoList(models.Model):
    organisation = models.OneToOneField(
        Organisation, on_delete=models.CASCADE, unique=True
    )

    def __str__(self) -> str:
        return '{} tasks'.format(self.organisation.name)


class Task(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    status = models.BooleanField(auto_created=True, default=False)
    todo_list_id = models.ForeignKey(
        ToDoList, on_delete=models.CASCADE, related_name='tasks'
    )

    def __str__(self) -> str:
        return self.name
