from django.contrib.auth import authenticate
from rest_framework import generics, mixins, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample

from .models import User
from .serializers import UserSerializer


def getObject(value):
    return User.objects.get(pk=value)

def getAllObjects():
    return User.objects.all()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        self.tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.tokens, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={201: OpenApiExample("Login realizado com sucesso", value={
            "refresh": "string",
            "access": "string"
        })}
    )
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Credenciais inválidas"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=201)
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    """Metodos HTTP com parametro"""
    def get(self, request, pk):
        """Obtem um usuario via id"""
        user = getObject(pk)
        if not user: return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Atualiza completamente um usuario via id"""
        user = getObject(pk)
        if not user: return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """Atualiza parcialmente um usuario via id"""
        user = getObject(pk)
        if not user: return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Deleta um usuario via id"""
        user = getObject(pk)
        if user:
            user.delete()
            return Response("Usuario deletado com sucesso", status=status.HTTP_204_NO_CONTENT)
        return Response("Usuario nao encontrado", status=status.HTTP_404_NOT_FOUND)