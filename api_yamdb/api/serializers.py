from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import exceptions, relations, serializers, validators
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор комментария"""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        exclude = ('id',)
        model = Genre


class WrittingTitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для записи."""

    genre = relations.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = relations.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title

    def validate_year(self, value):
        if value >= timezone.now().year:
            raise exceptions.ValidationError('Некорректный год создания')
        return value


class ReadingTitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для чтения."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        """Проверка на наличие двойного отзыва автора у одного произведения"""

        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise exceptions.ValidationError(
                    'Можно оставить только один отзыв к одному произведению'
                )
        return data


class TokenAccessObtainSerializer(TokenObtainSerializer):
    """Сериализатор для Access токена."""

    token_class = AccessToken
    username = serializers.CharField(max_length=255, required=True)
    confirmation_code = serializers.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(self, *args, **kwargs)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs.pop('username', None))
        if not user.confirmation_code.confirmation_code == attrs.pop(
            'confirmation_code', None
        ):
            raise exceptions.ValidationError(
                'Переданный confirmation_code не соответвует пользователю.'
            )
        access = self.get_token(user)
        attrs['access'] = str(access)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class UserSignUpSerializer(UserSerializer):
    """Сериализатор модели User для самостоятельной регистрации."""

    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta(UserSerializer.Meta):
        fields = ['email', 'username']

    def validate_username(self, value):
        """Исключение пересечения эндпоинтов."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class UserSerializerWithReadOnlyRole(UserSerializer):
    """Сериализатор модели User, но без возможности редактировать role."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']
