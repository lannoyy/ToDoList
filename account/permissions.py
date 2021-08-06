from organisation.models import Organisation
from rest_framework import permissions


class OrganisationPermission(permissions.BasePermission):
    """
    Permission check for access user to organisation.
    """

    def has_permission(self, request, view):
        return bool(Organisation.get_org_from_header(request))
