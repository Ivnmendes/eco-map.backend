from rest_framework import serializers

class GeocodeQuerySerializer(serializers.Serializer):
    address = serializers.CharField(required=True)

class ReverseGeocodeQuerySerializer(serializers.Serializer):
    lat = serializers.FloatField(required=True)
    lon = serializers.FloatField(required=True)

class GeocodeResultSerializer(serializers.Serializer):
    place_id = serializers.CharField()
    lat = serializers.CharField()
    lon = serializers.CharField()
    display_name = serializers.CharField()
