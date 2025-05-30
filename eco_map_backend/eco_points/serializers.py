from .models import CollectionPoint, CollectionType, PointRequest, PointReview, OperatingHour
from .validators import validate_latitude_value, validate_longitude_value, validate_category_value
from rest_framework import serializers
from .models import User

class OperatingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHour
        fields = ['id', 'collection_point', 'day_of_week', 'opening_time', 'closing_time', 'active']

    def validate_day_of_week(self, value):
        if not (1 <= value <= 7):
            raise serializers.ValidationError("O dia da semana deve ser um número entre 1 e 7")
        return value
    
    def validate(self, data):
        opening_time = data.get('opening_time')
        closing_time = data.get('closing_time')

        if opening_time and closing_time and opening_time >= closing_time:
            raise serializers.ValidationError({
                "Operating time error": "O horário do fechamento deve ser posterior ao de abertura."
            })

        return data

class CollectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = ['id', 'name', 'description']

class CollectionPointSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6)
    types = serializers.PrimaryKeyRelatedField(many=True, queryset=CollectionType.objects.all())
    operating_hours = OperatingHourSerializer(many=True, required=False)
    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'is_active', 'created_at', 'operating_hours']

    def get_types(self, obj):
        return [t.id for t in obj.types.all()]

class PointRequestSerializer(serializers.ModelSerializer):
    approved = serializers.BooleanField(read_only=True)
    latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6)
    types = serializers.PrimaryKeyRelatedField(many=True, queryset=CollectionType.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_name = serializers.CharField(read_only=True, source='user.first_name')
    # operating_hours = OperatingHourSerializer(many=True, required=False)

    class Meta:
        model = PointRequest
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'user', 'user_name', 'approved', 'created_at',
                   #operating_hours
                   ]

    def get_types(self, obj):
        return {str(t.id): t.name for t in obj.types.all()}
    
    def create(self, validated_data):
        validated_data['approved'] = False
        return super().create(validated_data)

class PointReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name')
    point_name = serializers.CharField(source='point.name', read_only=True)

    class Meta:
        model = PointReview
        fields = ['id', 'point', 'point_name', 'user', 'user_name', 'comment', 'created_at']
