# from accounts.models import User
from .models import CollectionPoint, CollectionType, PointRequest, PointReview
from .validators import validate_latitude_value, validate_longitude_value, validate_category_value
from rest_framework import serializers

class CollectionPointSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(validators=[validate_latitude_value]);
    longitude = serializers.DecimalField(validators=[validate_longitude_value]);
    types = serializers.CharField(validators=[validate_category_value])

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'created_by', 'is_active', 'created_at']

class CollectionType(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = ['id', 'name', 'description']

class PointRequest(serializers.ModelSerializer):
    class Meta:
        latitude = serializers.DecimalField(validators=[validate_latitude_value]);
        longitude = serializers.DecimalField(validators=[validate_longitude_value]);
        types = serializers.CharField(validators=[validate_category_value])
        
        model = PointRequest
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'user', 'approved', 'created_at']

class PointReview(serializers.ModelSerializer):
    class Meta:
        model = PointReview
        fields = ['id', 'point', 'user', 'comment', 'created_at']