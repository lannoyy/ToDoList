from to_do_lists.views import TasksViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'to_do_lists', TasksViewSet, basename='to_do_lists')
