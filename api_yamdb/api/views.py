import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import (filters, permissions, response, status, views,
                            viewsets)
from rest_framework_simplejwt.views import TokenViewBase

from api import serializers as api_serializers
from api.filters import TitleFilter
from api.mixins import CreateListDeleteViewSet
from api.permissions import (UserIsAuthorOrAdmin, UserRoleIsAllowedRole,
                             UserRoleIsAllowedRoleOrReadOnly)
from reviews.models import Category, Genre, Review, Title
from users.models import ConfirmationCode

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с произведениями."""

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = TitleFilter
    ordering = ('name',)

    permission_classes = [UserRoleIsAllowedRoleOrReadOnly]
    allowed_roles = [settings.ADMIN_ROLE]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return api_serializers.ReadingTitleSerializer
        return api_serializers.WrittingTitleSerializer


class CategoryViewSet(CreateListDeleteViewSet):
    """Представление для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = api_serializers.CategorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('$name',)
    ordering = ('slug',)
    lookup_field = 'slug'

    permission_classes = [UserRoleIsAllowedRoleOrReadOnly]
    allowed_roles = [settings.ADMIN_ROLE]


class GenreViewSet(CreateListDeleteViewSet):
    """Представление для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = api_serializers.GenreSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('$name',)
    ordering = ('slug',)
    lookup_field = 'slug'

    permission_classes = [UserRoleIsAllowedRoleOrReadOnly]
    allowed_roles = [settings.ADMIN_ROLE]


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для работы с комментариями к отзывам."""

    serializer_class = api_serializers.CommentsSerializer

    permission_classes = [UserRoleIsAllowedRoleOrReadOnly, UserIsAuthorOrAdmin]
    allowed_roles = [
        settings.USER_ROLE,
        settings.MODERATOR_ROLE,
        settings.ADMIN_ROLE,
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для работы с отзывами к произведениям."""

    serializer_class = api_serializers.ReviewSerializer

    permission_classes = [UserRoleIsAllowedRoleOrReadOnly, UserIsAuthorOrAdmin]
    allowed_roles = [
        settings.USER_ROLE,
        settings.MODERATOR_ROLE,
        settings.ADMIN_ROLE,
    ]

    def get_queryset(self):
        """Переопределение queryset."""

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение функции создания."""

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class TokenAccessObtainView(TokenViewBase):
    """
    Предоставляет пользователю Access токен.
    Требует в запросе передачу username и confirmation_code.
    """

    serializer_class = api_serializers.TokenAccessObtainSerializer


class UserSignUpView(views.APIView):
    """Представление для самостоятельной регистрации пользователей."""

    serializer_class = api_serializers.UserSignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Регистрация пользователя с отправкой кода подтверждения на email."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        confirmation_code = ConfirmationCode.objects.create(
            user=user, confirmation_code=str(uuid.uuid4())
        )
        message = f'confirmation_code: "{confirmation_code.confirmation_code}"'
        send_mail(
            'Сonfirmation code',
            message,
            settings.EMAIL_HOST_USER,
            [
                user.email,
            ],
            fail_silently=False,
        )

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class UserViewset(viewsets.ModelViewSet):
    """
    Реализация CRUD для модели пользователей (User).
    Доступно только администраторам.
    """

    queryset = User.objects.all()
    serializer_class = api_serializers.UserSerializer
    lookup_field = 'username'

    permission_classes = (UserRoleIsAllowedRole,)
    allowed_roles = [settings.ADMIN_ROLE]

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    ordering = ('username',)


class OwnAccountView(views.APIView):
    """
    Представление для получения данных о себе или частичного изменения.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Возвращает данные о пользователе, который сделал запрос."""
        serializer = api_serializers.UserSerializer(request.user)
        return response.Response(serializer.data)

    def patch(self, request):
        """Изменяет данные о пользователе, который сделал запрос."""
        serializer = api_serializers.UserSerializerWithReadOnlyRole(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
