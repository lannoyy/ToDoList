from django.db import models
import jwt
from django.shortcuts import get_object_or_404


class Organisation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_org_from_header(cls, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        org_name = jwt.decode(token, 'secret', algorithms=['HS256'])['organisation']
        organisation = get_object_or_404(cls, name=org_name)
        if organisation in request.user.organisations.all():
            return organisation

    @staticmethod
    def check_for_access(request, task):
        org = Organisation.get_org_from_header(request)
        return task.todo_list_id.organisation.name == org.name
