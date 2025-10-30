from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from rest_framework.decorators import action

from map.models.hazard_report import HazardReport
from map.serializers.hazard_report import HazardReportSerializer
class ReadAnyCreateAuthUpdateDeleteAdmin(permissions.BasePermission):
    """
    SAFE methods (GET, HEAD, OPTIONS): AllowAny
    POST: IsAuthenticated
    PUT/PATCH/DELETE: IsAdminUser
    """
    def has_permission(self, request, view):
        return True


class HazardReportViewSet(viewsets.ModelViewSet):
    """
    CRUD for HazardReport:
    - list (GET /hazard-reports/)
    - retrieve (GET /hazard-reports/{id}/)
    - create (POST /hazard-reports/)
    - update/partial_update (PUT/PATCH /hazard-reports/{id}/)
    - destroy (DELETE /hazard-reports/{id}/)
    """
    queryset = HazardReport.objects.all().order_by('-created_at')
    serializer_class = HazardReportSerializer
    permission_classes = [ReadAnyCreateAuthUpdateDeleteAdmin]

    # Enable search & ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'street_name', 'description', 'type', 'status', 'severity']
    ordering_fields = ['created_at', 'updated_at', 'street_name', 'status']

    # ------------------------
    # Swagger Documentation
    # ------------------------
    @swagger_auto_schema(
        operation_summary="List all hazard reports (optionally filter by user_id)",
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY,
                description='Filter reports by user_id (UUID)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description='Search by name, street_name, description, type, or status',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY,
                description='Order by created_at, updated_at, street_name, or status',
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 👉 Lọc theo user_id nếu có
        user_id = request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user__user_id=user_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="List all pending hazard reports",
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY,
                description='Optionally filter pending reports by user_id (UUID)',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: HazardReportSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='pending')
    def pending_reports(self, request):
        """
        Trả về tất cả report có status='pending', có thể lọc thêm theo user_id
        """
        user_id = request.query_params.get('user_id', None)
        queryset = HazardReport.objects.filter(status='pending')

        if user_id:
            queryset = queryset.filter(user__user_id=user_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="List all approve hazard reports",
        responses={200: HazardReportSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='approve')
    def approve_reports(self, request):
        queryset = HazardReport.objects.filter(status='approved')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Retrieve a hazard report by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new hazard report",
        request_body=HazardReportSerializer,
        responses={201: HazardReportSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Ghi thêm thời gian tạo
        serializer.save(created_at=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Update a hazard report (Admin only)",
        request_body=HazardReportSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a hazard report (Admin only)",
        request_body=HazardReportSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a hazard report (Admin only)")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
