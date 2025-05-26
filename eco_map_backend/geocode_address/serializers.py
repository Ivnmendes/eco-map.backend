from rest_framework import serializers

class SimplifiedGeocodeQuerySerializer(serializers.Serializer):
    """
    Serializer para validação dos parâmetros de entrada da geocodificação simplificada.
    """
    street = serializers.CharField(required=True, max_length=255)
    number = serializers.CharField(required=False, max_length=10, allow_blank=True)
    neighborhood = serializers.CharField(required=False, max_length=100, allow_blank=True)
    postcode = serializers.CharField(required=False, max_length=10, allow_blank=True)

class ReverseGeocodeQuerySerializer(serializers.Serializer):
    """
    Serializer para validação dos parâmetros de entrada da geocodificação inversa.
    """
    lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6)

class GeocodeResultSerializer(serializers.Serializer):
    """
    Serializer para formatar o resultado da geocodificação.
    """
    place_id = serializers.CharField()
    lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6)
    display_name = serializers.CharField()

class SimplifiedReverseGeocodeResultSerializer(serializers.Serializer):
    """
    Serializer para formatar o resultado da geocodificação inversa
    com apenas os campos simplificados (rua, número, bairro, CEP, cidade, estado).
    """
    street = serializers.CharField(source='address.road', allow_null=True, required=False)
    number = serializers.CharField(source='address.house_number', allow_null=True, required=False)
    neighborhood = serializers.CharField(source='address.suburb', allow_null=True, required=False)
    postcode = serializers.CharField(source='address.postcode', allow_null=True, required=False)
    city = serializers.CharField(source='address.city', allow_null=True, required=False)
    state = serializers.CharField(source='address.state', allow_null=True, required=False)