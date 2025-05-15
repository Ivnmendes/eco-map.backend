from .models import CollectionPoint, CollectionType, PointRequest, PointReview
from .validators import validate_latitude_value, validate_longitude_value, validate_category_value
from rest_framework import serializers

class CollectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = ['id', 'name', 'description']

class CollectionPointSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6);
    longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6);
    types = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='created_by.first_name')

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'created_by', 'user_name', 'is_active', 'created_at']

    def get_types(self, obj):
        return {str(t.id): t.name for t in obj.types.all()}

class PointRequestSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6)
    types = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.first_name')

    class Meta:
        model = PointRequest
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'user', 'user_name', 'approved', 'created_at']

    def get_types(self, obj):
        return {str(t.id): t.name for t in obj.types.all()}

class PointReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name')
    point_name = serializers.CharField(source='point.name', read_only=True)

    class Meta:
        model = PointReview
        fields = ['id', 'point', 'point_name', 'user', 'user_name', 'comment', 'created_at']