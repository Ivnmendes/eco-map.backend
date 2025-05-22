# views.py
import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import GeocodeQuerySerializer, ReverseGeocodeQuerySerializer, GeocodeResultSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(name='address', type=str, required=True, location=OpenApiParameter.QUERY)
    ],
    responses={200: GeocodeResultSerializer},
    tags=['Geo codificação']
)
class GeocodeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        address = request.query_params.get('address')
        if not address:
            return Response({"error": "Parâmetro 'address' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"geocode:{address.lower()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": address, "format": "json", "limit": 1},
                headers={"User-Agent": "EcoPoints/1.0"},
                timeout=5
            )
            data = response.json()
            if not data:
                return Response({"error": "Endereço não encontrado."}, status=404)

            cache.set(cache_key, data[0], timeout=86400)
            return Response(data[0])

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    parameters=[
        OpenApiParameter(name='lat', type=float, required=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='lon', type=float, required=True, location=OpenApiParameter.QUERY)
    ],
    responses={200: GeocodeResultSerializer},
    tags=['Geo codificação']
)
class ReverseGeocodeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')

        if not lat or not lon:
            return Response({"error": "Parâmetros 'lat' e 'lon' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"reverse:{lat}:{lon}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

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
            data = response.json()

            if "error" in data:
                return Response({"error": data["error"]}, status=404)

            cache.set(cache_key, data, timeout=86400)
            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
