from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from .models import CollectionType, CollectionPoint, PointRequest, PointReview, PointRequest, OperatingHour
from .serializers import CollectionPointSerializer, CollectionTypeSerializer, PointRequestSerializer, PointReviewSerializer, OperatingHourSerializer

def get_all_object_collection_type():
    return CollectionType.objects.all()

def get_all_object_collection_point():
    return CollectionPoint.objects.all()

def get_all_object_operating_hour():
    return OperatingHour.objects.all()

def get_all_object_point_request():
    return PointRequest.objects.all()

def get_all_object_point_review():
    return PointReview.objects.all()

@extend_schema(tags=["Tipo de coleta"])
class CollectionTypeList(generics.ListCreateAPIView):
    """
    Responsável por lidar com operações para vários tipos de coleta (getAll)
    """
    queryset = get_all_object_collection_type()
    serializer_class = CollectionTypeSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Tipo de coleta"])
class CollectionTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Responsável por lidar com operações especificas por tipo de coleta (via id)
    """
    queryset = get_all_object_collection_type()
    serializer_class = CollectionTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

@extend_schema(tags=["Ponto de coleta"])
class CollectionPointList(generics.ListCreateAPIView):
    """
    Responsável por lidar com operações para vários pontos de coleta (getAll)
    """
    queryset = get_all_object_collection_point()
    serializer_class = CollectionPointSerializer
    permission_classes = [IsAuthenticated]
    
@extend_schema(tags=["Ponto de coleta"])
class CollectionPointDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Responsável por lidar com operações especificas por ponto de coleta (via id)
    """
    queryset = get_all_object_collection_point()
    serializer_class = CollectionPointSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

@extend_schema(tags=["Horário de funcionamento (ponto de coleta)"])
class OperatingHourList(generics.ListCreateAPIView):
    """
    Lista todos os horários de funcionamento de todos os pontos de coleta ou
    cria um novo horário de funcionamento.
    Ao criar, 'collection_point_id' deve ser fornecido no corpo da requisição.
    """
    queryset = get_all_object_operating_hour()
    serializer_class = OperatingHourSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Horário de funcionamento (ponto de coleta)"])
class OperatingHourDetail(generics.ListCreateAPIView):
    """
    Lista todos os horários de funcionamento de um ponto de coleta específico ou
    cria um novo horário de funcionamento para esse ponto de coleta.
    O ID do ponto de coleta é esperado como um parâmetro na URL (ex: /api/collection-points/<collection_point_pk>/operating-hours/).
    """
    serializer_class = OperatingHourSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna uma lista de horários de funcionamento apenas para o ponto de coleta
        especificado no parâmetro 'collection_point_pk' da URL.
        """
        collection_point_pk = self.kwargs.get('collection_point_pk')
        if collection_point_pk is not None:
            return OperatingHour.objects.filter(collection_point_id=collection_point_pk)
        return OperatingHour.objects.none() # Ou levante um erro 404 se o pk não for fornecido e for obrigatório
    
    def perform_create(self, serializer):
        """
        Associa automaticamente o novo horário de funcionamento ao ponto de coleta
        especificado no parâmetro 'collection_point_pk' da URL.
        """
        collection_point_pk = self.kwargs.get('collection_point_pk')
        serializer.save(collection_point_id=collection_point_pk)

@extend_schema(tags=["Avaliação do ponto"])
class PointReviewList(generics.ListCreateAPIView):
    """
    Responsável por lidar com operações especificas por review do ponto (getAll)
    """
    queryset = get_all_object_point_review()
    serializer_class = PointReviewSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Avaliação do ponto"])
class PointReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Responsável por lidar com operações especificas por review do ponto (via id)
    """
    queryset = get_all_object_point_review()
    serializer_class = PointReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

@extend_schema(
    tags=["Avaliação do ponto"],
    parameters=[
        OpenApiParameter(name="user_id", required=False, description="ID do usuário", type=int),
        OpenApiParameter(name="point_id", required=False, description="ID do ponto de coleta", type=int),
    ]
)
class PointReviewFilteredList(APIView):
    """
    Retorna avaliações filtradas por usuário e/ou ponto de coleta.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        point_id = request.query_params.get('id')

        queryset = PointReview.objects.all()

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if point_id:
            queryset = queryset.filter(collection_point_id=point_id)

        serializer = PointReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Requisição de novo ponto"])
class PointRequestList(generics.ListCreateAPIView):
    """
    Responsável por lidar com operações especificas por requisição de ponto (getAll)
    """
    queryset = get_all_object_point_request()
    serializer_class = PointRequestSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Requisição de novo ponto"])
class PointRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Responsável por lidar com operações especificas por requisição de ponto (via id)
    """
    queryset = get_all_object_point_request()
    serializer_class = PointRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'