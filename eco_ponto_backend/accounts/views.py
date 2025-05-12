from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

def getObject(value):
    return User.objects.get(pk=value)

def getAllObjects():
    return User.objects.all()

class UserList(APIView):
    def get(self, request):
        users = getAllObjects()
        if not users: return Response("Nenhum usuario encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get(self, request, pk):
        user = getObject(pk)
        if not user: return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        user = getObject(pk)
        if not user: return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = getObject(pk)
        if not user: return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = getObject(pk)
        if user:
            user.delete()
            return Response("Usuario deletado com sucesso", status=status.HTTP_204_NO_CONTENT)
        return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)