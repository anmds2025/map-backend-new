from datetime import timedelta
import uuid
from django.utils import timezone
from django.db import models

from map.models.user import User


class HazardReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.TextField(default="")
    user = models.ForeignKey(
        User,
        to_field='user_id', 
        on_delete=models.CASCADE,
        related_name='hazard_reports',
        null=True,
        db_column='user_id'  
    )

    # Location fields
    street_name = models.TextField(default="")
    latitude = models.TextField(default="")
    longitude = models.TextField(default="")

    # Description
    description = models.TextField(blank=True, help_text="Detailed description in English")
    type = models.TextField(default="")
    status = models.TextField(default="pending")
    severity = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hazard_report'
        indexes = [ 
            models.Index(fields=['street_name']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['created_at']),
        ]
