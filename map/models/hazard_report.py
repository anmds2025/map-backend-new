from datetime import timedelta
import uuid
from django.utils import timezone
from django.db import models


class HazardReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.TextField(default="")

    # Location fields
    street_name = models.TextField(default="")
    latitude = models.TextField(default="")
    longitude = models.TextField(default="")

    # Description
    description = models.TextField(blank=True, help_text="Detailed description in English")


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hazard_report'
        indexes = [ 
            models.Index(fields=['street_name']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['created_at']),
        ]
