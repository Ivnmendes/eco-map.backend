from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CollectionType, CollectionPoint, PointRequest, PointReview, PointRequest
from .serializers import CollectionPointSerializer, CollectionTypeSerializer, PointRequestSerializer, PointReviewSerializer

def get_object_collection_type(value):
    return CollectionType.objects.get(pk=value)

def get_all_object_collection_type():
    return CollectionType.objects.all()

def get_object_collection_point(value):
    return CollectionPoint.objects.get(pk=value)

def get_all_object_collection_point():
    return CollectionPoint.objects.all()

def get_object_point_request(value):
    return PointRequest.objects.get(pk=value)

def get_all_object_point_request():
    return PointRequest.objects.all()

def get_object_point_review(value):
    return PointReview.objects.get(pk=value)

def get_all_object_point_review():
    return PointReview.objects.all()

class CollectionTypeList(APIView):
    def get(self, request):
        collectionTypes = get_all_object_collection_type()
        if not collectionTypes: return Response("Nenhuma categoria de coleta", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionTypeSerializer(collectionTypes, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CollectionTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionTypeDetail(APIView):
    def get(self, request, pk):
        collectionType = get_object_collection_type(pk)
        if not collectionType: return Response("Categoria nao encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionTypeSerializer(collectionType)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        collectionType = get_object_collection_type(pk)
        if not collectionType: return Response("Categoria nao encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionTypeSerializer(collectionType, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        collectionType = get_object_collection_type(pk)
        if not collectionType: return Response("Categoria nao encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionTypeSerializer(collectionType, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collectionType = get_object_collection_type(pk)
        if collectionType:
            collectionType.delete()
            return Response("Categoria deletada com sucesso", status=status.HTTP_204_NO_CONTENT)
        return Response("Categoria nao encontrada", status=status.HTTP_404_NOT_FOUND)

class CollectionPointList(APIView):
    def get(self, request):
        collectionPoints = get_all_object_collection_point()
        if not collectionPoints: return Response("Nenhum ponto de coleta encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionPointSerializer(collectionPoints, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CollectionPointSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CollectionPointDetail(APIView):
    def get(self, request, pk):
        collectionPoint = get_object_collection_point(pk)
        if not collectionPoint: return Response("Ponto de coleta não encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionPointSerializer(collectionPoint)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        collectionPoint = get_object_collection_point(pk)
        if not collectionPoint: return Response("Ponto de coleta não encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionPointSerializer(collectionPoint, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        collectionPoint = get_object_collection_point(pk)
        if not collectionPoint: return Response("Ponto de coleta não encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionPointSerializer(collectionPoint, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collectionPoint = get_object_collection_point(pk)
        if collectionPoint:
            collectionPoint.delete()
            return Response("Ponto de coleta criado com sucesso", status=status.HTTP_204_NO_CONTENT)
        return Response("Ponto de coleta não encontrado", status=status.HTTP_404_NOT_FOUND)   

class PointReviewList(APIView):
    def get(self, request):
        pointReview = get_all_object_point_review()
        if not pointReview: return Response("Nenhum ponto em análise", status=status.HTTP_404_NOT_FOUND)

        serializer = PointReviewSerializer(pointReview, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PointReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PointReviewDetail(APIView):
    def get(self, request, pk):
        PointReview = get_object_point_review(pk)
        if not PointReview: return Response("Avaliação não encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = PointReviewSerializer(PointReview)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        PointReview = get_object_point_review(pk)
        if not PointReview: return Response("Avaliação não encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = PointReviewSerializer(PointReview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        PointReview = get_object_point_review(pk)
        if not PointReview: return Response("Avaliação não encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = PointReviewSerializer(PointReview, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        PointReview = get_object_point_review(pk)
        if PointReview:
            PointReview.delete()
            return Response("Avaliação submetida com sucesso", status=status.HTTP_204_NO_CONTENT)
        return Response("Avaliação não encontrada", status=status.HTTP_404_NOT_FOUND)   

class PointRequestList(APIView):
    def get(self, request):
        pointRequest = get_all_object_point_request()
        if not pointRequest: return Response("Nenhum ponto em análise", status=status.HTTP_404_NOT_FOUND)

        serializer = PointRequestSerializer(pointRequest, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PointRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PointRequestDetail(APIView):
    def get(self, request, pk):
        PointRequest = get_object_point_request(pk)
        if not PointRequest: return Response("Nenhum ponto em análise", status=status.HTTP_404_NOT_FOUND)

        serializer = PointRequestSerializer(PointRequest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        PointRequest = get_object_point_request(pk)
        if not PointRequest: return Response("Nenhum ponto em análise", status=status.HTTP_404_NOT_FOUND)

        serializer = PointRequestSerializer(PointRequest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        PointRequest = get_object_point_request(pk)
        if not PointRequest: return Response("Nenhum ponto em análise", status=status.HTTP_404_NOT_FOUND)

        serializer = PointRequestSerializer(PointRequest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        PointRequest = get_object_point_request(pk)
        if PointRequest:
            PointRequest.delete()
            return Response("Ponto de coleta enviado para análise", status=status.HTTP_204_NO_CONTENT)
        return Response("Nenhum ponto em análise", status=status.HTTP_404_NOT_FOUND)   