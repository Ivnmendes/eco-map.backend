from django.contrib.auth import authenticate
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, inline_serializer

from .models import User
from .serializers import LoginSerializer, LogoutSerializer, UserSerializer

def getAllObjects():
    return User.objects.all()

@extend_schema(tags=["Autenticação"])
class RegisterView(generics.CreateAPIView):
    queryset = getAllObjects()
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
        super().create(request, *args, **kwargs)
        return Response(self.tokens, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=["Autenticação"],
    request=LoginSerializer,
    responses={
        201: inline_serializer(
            name="LoginResponse",
            fields={
                "refresh": serializers.CharField(),
                "access": serializers.CharField()
            }
        ),
        401: inline_serializer(
            name="LoginError",
            fields={
                "error": serializers.CharField()
            }
        )
    },
    examples=[
        OpenApiExample(
            name="Exemplo de login",
            value={"email": "usuario@email.com", "password": "senha123"},
            request_only=True
        )
    ]
)
class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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
    

@extend_schema(
    tags=["Autenticação"],
    request=LogoutSerializer,
    responses={205: None, 400: None}
)
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema_view(
    post=extend_schema(tags=['Autenticação'])
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=["Usuários"])
class UserList(generics.ListAPIView):
    queryset = getAllObjects()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Usuários"])
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = getAllObjects()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'