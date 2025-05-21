from django.contrib.auth import authenticate
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, inline_serializer

from .models import User
from .serializers import LoginSerializer, LogoutSerializer, UserSerializer, UserMeSerializer

def getAllObjects():
    return User.objects.all()

@extend_schema(tags=["Autenticação"])
class RegisterView(generics.CreateAPIView):
    """
    Cria novo usuário
    """
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
            value={"email": "teste@email.com", "password": "teste123#"},
            request_only=True
        )
    ]
)
class LoginView(generics.GenericAPIView):
    """
    Realiza login
    """
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
    
@extend_schema(tags=["Autenticação"])
class MeView(generics.GenericAPIView):
    """
    Retorna informações sobre o usuário do request
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

@extend_schema(
    tags=["Autenticação"],
    request=LogoutSerializer,
    responses={205: None, 400: None}
)
class LogoutView(generics.GenericAPIView):
    """
    Responsável por deslogar o usuário, adicionando o token ao blacklist
    """
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
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema_view(
    post=extend_schema(tags=['Autenticação'])
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema_view(
    post=extend_schema(tags=['Autenticação'])
)
class CustomTokenVerifyView(TokenVerifyView):
    pass

@extend_schema(tags=["Usuários"])
class UserList(generics.ListAPIView):
    """
    Responsável por lidar com operações para vários usuários (getAll)
    """
    queryset = getAllObjects()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restringe acesso de listagem/detalhamento apenas para admin.
        """
        user = self.request.user
        if self.request.method in ['GET']:
            if not user.is_staff and not user.is_admin:
                raise PermissionDenied("Apenas administradores tem acesso a essas rotas")
        return super().get_queryset()

@extend_schema(tags=["Usuários"])
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Responsável por lidar com operações especificas por usuário (via id)
    """
    queryset = getAllObjects()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Restringe acesso de listagem/detalhamento apenas para admin.
        """
        user = self.request.user
        if self.request.method in ['GET']:
            if not user.is_staff and not user.is_admin:
                raise PermissionDenied("Apenas administradores tem acesso a essas rotas")
        return super().get_queryset()
    
    def perform_update(self, serializer):
        """
        Impede edição de outro usuário que não seja o dono.
        """
        user = self.request.user
        if user != self.get_object() or not user.is_staff and user.is_admin:
            raise PermissionDenied("Você só pode editar sua própria conta.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Impede exclusão de outro usuário que não seja o dono.
        """
        user = self.request.user
        if user != instance or not user.is_staff and user.is_admin:
            raise PermissionDenied("Você só pode excluir sua própria conta.")
        instance.delete()