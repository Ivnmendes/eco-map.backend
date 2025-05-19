from rest_framework import serializers

def validate_latitude_value(value):
    if value <= -90.0 and value >= 90.0:
        return serializers.ValidationError("Latitude inválida.")
    return value

def validate_longitude_value(value):
    if value <= -180.0 and value >= 180.0:
        return serializers.ValidationError("Longitude inválida.")
    return value

def validate_category_value(value):
    allowed = ['orgânico', 'reciclável', 'perigoso']
    if value not in allowed:
        raise serializers.ValidationError("Categoria inválida.")
    return value
