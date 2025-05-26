# views.py
import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import SimplifiedGeocodeQuerySerializer, ReverseGeocodeQuerySerializer, GeocodeResultSerializer, SimplifiedReverseGeocodeResultSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='street',
            type=OpenApiTypes.STR,
            required=True,
            location=OpenApiParameter.QUERY,
            description="Nome da rua para geocodificação."
        ),
        OpenApiParameter(
            name='number',
            type=OpenApiTypes.STR,
            required=False,
            location=OpenApiParameter.QUERY,
            description="Número do imóvel (opcional)."
        ),
        OpenApiParameter(
            name='neighborhood',
            type=OpenApiTypes.STR,
            required=False,
            location=OpenApiParameter.QUERY,
            description="Nome do bairro (opcional)."
        ),
        OpenApiParameter(
            name='postcode',
            type=OpenApiTypes.STR,
            required=False,
            location=OpenApiParameter.QUERY,
            description="CEP do endereço (opcional)."
        ),
    ],
    responses={200: GeocodeResultSerializer},
    tags=['Geo codificação']
)
class GeocodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = SimplifiedGeocodeQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        street = validated_data.get('street')
        number = validated_data.get('number')
        neighborhood = validated_data.get('neighborhood')
        postcode = validated_data.get('postcode')

        city = "Santa Maria"
        state = "Rio Grande do Sul"
        country = "Brazil"

        address_parts = [street]
        if number:
            address_parts.append(number)
        if neighborhood:
            address_parts.append(neighborhood)
        address_parts.append(city)
        address_parts.append(state)
        if postcode:
            address_parts.append(postcode)
        address_parts.append(country)

        query_address = ", ".join(filter(None, address_parts))

        cache_key = f"geocode:{query_address.lower()}"
        cached = cache.get(cache_key)
        if cached:
            output_serializer = GeocodeResultSerializer(cached)
            return Response(output_serializer.data)

        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query_address, "format": "json", "limit": 1},
                headers={"User-Agent": "EcoPoints/1.0"},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                return Response({"error": "Endereço não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            result_data = data[0]

            cache.set(cache_key, result_data, timeout=86400)

            output_serializer = GeocodeResultSerializer(result_data)
            return Response(output_serializer.data)

        except requests.exceptions.Timeout:
            return Response({"error": "Tempo limite de conexão com o servidor de geocodificação excedido."}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Erro ao conectar com o serviço de geocodificação: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    request=ReverseGeocodeQuerySerializer,
    parameters=[
        OpenApiParameter(
            name='lat',
            type=OpenApiTypes.DECIMAL,
            required=True,
            location=OpenApiParameter.QUERY,
            description="Latitude para geocodificação inversa."
        ),
        OpenApiParameter(
            name='lon',
            type=OpenApiTypes.DECIMAL,
            required=True,
            location=OpenApiParameter.QUERY,
            description="Longitude para geocodificação inversa."
        ),
    ],
    
    responses={200: SimplifiedReverseGeocodeResultSerializer},
    tags=['Geo codificação']
)
class ReverseGeocodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = ReverseGeocodeQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        lat = validated_data.get('lat')
        lon = validated_data.get('lon')

        cache_key = f"reverse:{lat}:{lon}"
        cached = cache.get(cache_key)
        if cached:
            output_serializer = SimplifiedReverseGeocodeResultSerializer(cached)
            return Response(output_serializer.data)

        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={
                    "lat": lat,
                    "lon": lon,
                    "format": "json",
                    "addressdetails": 1
                },
                headers={"User-Agent": "EcoPoints/1.0"},
                timeout=5
            )
            response.raise_for_status()
            nominatim_data = response.json()

            if "error" in nominatim_data:
                return Response({"error": nominatim_data["error"]}, status=status.HTTP_404_NOT_FOUND)

            cache.set(cache_key, nominatim_data, timeout=86400)

            output_serializer = SimplifiedReverseGeocodeResultSerializer(nominatim_data)
            return Response(output_serializer.data)

        except requests.exceptions.Timeout:
            return Response({"error": "Tempo limite de conexão com o servidor de geocodificação excedido."}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Erro ao conectar com o serviço de geocodificação: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)