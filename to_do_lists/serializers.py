from rest_framework import serializers

from to_do_lists.models import ToDoList, Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'description']
        write_only_fields = ['todo_list_id']
        read_only_fields = ['id']
    

class ToDoListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source=ToDoList.organisation.field.name)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ['name', 'tasks']
