from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .functions import distance, send_email, watermark
from .models import CustomUser, Match
from .serializers import (CustomObtainAuthTokenSerializer,
                          CustomUserSerializer, ListUserSerializer)


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Сздает пользователя. Доступен только POST запрос.
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
        serializer = ListUserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Выдает пользователю токен при авторизации.
    """
    serializer_class = CustomObtainAuthTokenSerializer


class MatchViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    Создает обьекты лайка между пользователями.
    Отправляет письма пользователям если у них Match.
    """
    queryset = Match.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = None

    def list(self, request, *args, **kwargs):
        user = request.user
        user_like = get_object_or_404(CustomUser,
                                      id=self.kwargs.get('user_id'))
        exist = Match.objects.filter(user=user,
                                     user_like=user_like).exists()

        if user == user_like:
            return Response({'Нельзя лайкнуть самого себя.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif exist:
            return Response({'Вы уже поставили лайк этому пользователю!'},
                            status=status.HTTP_400_BAD_REQUEST)

        Match.objects.create(user=user, user_like=user_like)
        match = Match.objects.filter(user=user_like, user_like=user).exists()

        if match:
            send_email(user, user_like)
            send_email(user_like, user)
        return Response({'Лайк поставлен!'}, status=status.HTTP_201_CREATED)


class ListViewSet(viewsets.ModelViewSet):
    """
    Отображает список всех пользователей.
    Фильтрация по полям 'sex', 'first_name', 'last_name
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ListUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sex', 'first_name', 'last_name']

    def get_queryset(self):
        """
        Определяет расстояние до всех пользователей.
        Если пользователь в зоне поражения - добавляет в список и отображает
        его.
        """
        if self.request.query_params.get('distance'):
            dist = self.request.query_params.get('distance')
            users = []
            for client in self.queryset:
                if distance(client.lat, client.lon, self.request.user.lat,
                            self.request.user.lon) <= int(dist):
                    users.append(client)
            return self.queryset.filter(email__in=users)
        return self.queryset
