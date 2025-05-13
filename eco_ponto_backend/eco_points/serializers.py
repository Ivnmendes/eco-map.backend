from .models import CollectionPoint, CollectionType, PointRequest, PointReview
from .validators import validate_latitude_value, validate_longitude_value, validate_category_value
from rest_framework import serializers

class CollectionPointSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6);
    longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6);
    types = serializers.PrimaryKeyRelatedField(
        validators=[validate_category_value],
        many=True,
        queryset=CollectionType.objects.all()
    )

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'created_by', 'is_active', 'created_at']

class CollectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = ['id', 'name', 'description']

class PointRequestSerializer(serializers.ModelSerializer):
    class Meta:
        latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6)
        longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6)
        types = serializers.CharField(validators=[validate_category_value])
        
        model = PointRequest
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'user', 'approved', 'created_at']

class PointReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointReview
        fields = ['id', 'point', 'user', 'comment', 'created_at']