from organisation.models import Organisation
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from account.permissions import OrganisationPermission
from rest_framework.response import Response
from account.auth import CustomAuthentication
from to_do_lists.serializers import ToDoListSerializer, TaskSerializer
from to_do_lists.models import Task, ToDoList
from drf_yasg.utils import swagger_auto_schema


class TasksViewSet(viewsets.ViewSet):

    authentication_classes = [CustomAuthentication]
    permission_classes = [OrganisationPermission]

    @swagger_auto_schema(responses={200: ToDoListSerializer})
    def list(self, request):
        organisation = Organisation.get_org_from_header(request)
        to_do_list = ToDoList.objects.get_or_create(organisation=organisation)[0]
        serializer = ToDoListSerializer(to_do_list)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: TaskSerializer})
    def retrieve(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if not Organisation.check_for_access(request, task):
            return Response({'error': 'no access'})
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: TaskSerializer}, request_body=TaskSerializer)
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        org = Organisation.get_org_from_header(request)
        to_do_list = ToDoList.objects.get_or_create(organisation=org)[0]
        if serializer.is_valid():
            serializer.save(todo_list_id=to_do_list)
            return Response(serializer.data)
        return Response(serializer.errors)

    @swagger_auto_schema(responses={200: TaskSerializer}, request_body=TaskSerializer)
    def update(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if not Organisation.check_for_access(request, task):
            return Response({'error': 'no access'})
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.update(task, request.data)
            return Response(serializer.data)
        return Response(serializer.errors)

    @swagger_auto_schema(responses={200: TaskSerializer}, request_body=TaskSerializer)
    def partial_update(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if not Organisation.check_for_access(request, task):
            return Response({'error': 'no access'})
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(task, request.data)
            return Response(serializer.data)
        return Response(serializer.errors)

    @swagger_auto_schema(responses={200: TaskSerializer}, request_body=TaskSerializer)
    def destroy(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if not Organisation.check_for_access(request, task):
            return Response({'error': 'no access'})
        data = TaskSerializer(task).data
        task.delete()
        return Response(data)
