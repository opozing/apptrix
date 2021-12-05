from .models import CustomUser

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, mixins
from .serializers import CustomUserSerializer, CustomObtainAuthTokenSerializer
from .functions import watermark


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Сздает пользователя
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Хеширует пароль для получения токена.
        Накладывает водяной знак на аватарку.
        """
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        password = serializer.data['password']
        email = serializer.data['email']
        user = CustomUser.objects.get(email=email)
        user.set_password(password)
        watermark(user.avatar)
        user.save()
        serializer = CustomUserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomObtainAuthTokenSerializer
