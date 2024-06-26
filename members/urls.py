from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectMemberViewSet

router = DefaultRouter()
router.register(r'members', ProjectMemberViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
