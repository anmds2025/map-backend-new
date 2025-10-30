# map/serializers/hazard_report.py
from rest_framework import serializers
from map.models.hazard_report import HazardReport

class HazardReportSerializer(serializers.ModelSerializer):
    # Model đang dùng TextField cho lat/long, ta vẫn validate phạm vi số:
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    user_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = HazardReport
        fields = ['id', 'name', 'description', 'street_name', 'latitude', 'longitude', 'status', 'type', 'severity', 'user_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        lat = attrs.get('latitude', None)
        lon = attrs.get('longitude', None)

        # ✅ Chỉ validate nếu có truyền vào
        if lat is not None and lon is not None:
            try:
                lat_f = float(lat)
                lon_f = float(lon)
            except (TypeError, ValueError):
                raise serializers.ValidationError("latitude and longitude must be numeric.")

            if not (-90.0 <= lat_f <= 90.0):
                raise serializers.ValidationError("latitude must be between -90 and 90.")
            if not (-180.0 <= lon_f <= 180.0):
                raise serializers.ValidationError("longitude must be between -180 and 180.")
        
        return attrs
