from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema, OpenApiExample

from .models import CollectionType, CollectionPoint, PointRequest, PointReview, PointRequest
from .serializers import CollectionPointSerializer, CollectionTypeSerializer, PointRequestSerializer, PointReviewSerializer

def get_all_object_collection_type():
    return CollectionType.objects.all()

def get_all_object_collection_point():
    return CollectionPoint.objects.all()

def get_all_object_point_request():
    return PointRequest.objects.all()

def get_all_object_point_review():
    return PointReview.objects.all()

@extend_schema(tags=["Tipo de coleta"])
class CollectionTypeList(generics.ListAPIView):
    queryset = get_all_object_collection_type()
    serializer_class = CollectionTypeSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Tipo de coleta"])
class CollectionTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_object_collection_type()
    serializer_class = CollectionTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

@extend_schema(tags=["Ponto de coleta"])
class CollectionPointList(generics.ListAPIView):
    queryset = get_all_object_collection_point()
    serializer_class = CollectionPointSerializer
    permission_classes = [IsAuthenticated]
    
@extend_schema(tags=["Ponto de coleta"])
class CollectionPointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_object_collection_point()
    serializer_class = CollectionPointSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


@extend_schema(tags=["Avaliação do ponto"])
class PointReviewList(generics.ListAPIView):
    queryset = get_all_object_point_review()
    serializer_class = PointReviewSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Avaliação do ponto"])
class PointReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_object_point_review()
    serializer_class = PointReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

@extend_schema(tags=["Requisição de novo ponto"])
class PointRequestList(generics.ListAPIView):
    queryset = get_all_object_point_request()
    serializer_class = PointRequestSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Requisição de novo ponto"])
class PointRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_object_point_request()
    serializer_class = PointRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'