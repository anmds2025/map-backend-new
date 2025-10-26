# map/views/hazard_report.py
from rest_framework import viewsets, permissions, filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from map.models.hazard_report import HazardReport
from map.serializers.hazard_report import HazardReportSerializer

class ReadAnyCreateAuthUpdateDeleteAdmin(permissions.BasePermission):
    """
    SAFE methods (GET, HEAD, OPTIONS): AllowAny
    POST: IsAuthenticated
    PUT/PATCH/DELETE: IsAdminUser
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff  # admin for update/delete

class HazardReportViewSet(viewsets.ModelViewSet):
    """
    CRUD for HazardReport:
    - list  (GET /hazard-reports/)
    - retrieve (GET /hazard-reports/{id}/)
    - create (POST /hazard-reports/)
    - update/partial_update (PUT/PATCH /hazard-reports/{id}/)
    - destroy (DELETE /hazard-reports/{id}/)
    """
    queryset = HazardReport.objects.all().order_by('-created_at')
    serializer_class = HazardReportSerializer
    permission_classes = [ReadAnyCreateAuthUpdateDeleteAdmin]

    # Search & ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'street_name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'street_name']

    @swagger_auto_schema(
        operation_summary="List hazard reports",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search by name, street_name, description', type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description='created_at,-created_at, updated_at, street_name', type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a hazard report by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new hazard report")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a hazard report")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Partially update a hazard report")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a hazard report")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
