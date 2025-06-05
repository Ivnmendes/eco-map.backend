from .models import CollectionPoint, CollectionType, PointReview, OperatingHour, PointImage
from .validators import validate_latitude_value, validate_longitude_value, validate_category_value
from rest_framework import serializers

class OperatingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingHour
        fields = ['day_of_week', 'opening_time', 'closing_time', 'active']

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

class PointImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointImage
        fields = ['id', 'collection_point', 'image']
    
    def validate_image(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("A imagem deve ser um arquivo PNG ou JPEG.")
        return value
    
class PointImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = PointImage
        fields = ['image']

class CollectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = ['id', 'name', 'description']

class CollectionPointSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(validators=[validate_latitude_value], max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(validators=[validate_longitude_value], max_digits=9, decimal_places=6)
    types = serializers.PrimaryKeyRelatedField(many=True, queryset=CollectionType.objects.all())
    operating_hours = OperatingHourSerializer(many=True, required=True)
    images = PointImageSerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(read_only=True) 
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = CollectionPoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'types', 'is_active', 'created_at', 'operating_hours', 'images', 'user', 'user_name']
    
    def create(self, validated_data):
        operating_hours_data = validated_data.pop('operating_hours', [])
        types_data = validated_data.pop('types', [])
        
        validated_data['is_active'] = False

        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data['user'] = request.user
        
        collection_point = CollectionPoint.objects.create(**validated_data)
        
        collection_point.types.set(types_data)
        
        for op_hour_data in operating_hours_data:
            OperatingHour.objects.create(collection_point=collection_point, **op_hour_data)

        return collection_point

class PointReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name')
    point_name = serializers.CharField(source='point.name', read_only=True)

    class Meta:
        model = PointReview
        fields = ['id', 'point', 'point_name', 'user', 'user_name', 'comment', 'created_at']
