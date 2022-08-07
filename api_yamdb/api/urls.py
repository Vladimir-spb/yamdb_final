from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from api import views

API_VERSION = 'v1'


router_v1 = routers.DefaultRouter()
router_v1.register('users', views.UserViewset, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments/(?P<comment_id>\d+)',
    views.CommentViewSet,
    basename='comment',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    views.ReviewViewSet,
    basename='review',
)
router_v1.register(r'titles', views.TitleViewSet, basename='titles')
router_v1.register(r'categories', views.CategoryViewSet, basename='categories')
router_v1.register(r'genres', views.GenreViewSet, basename='genres')


app_name = 'api'
urlpatterns = [
    path(
        f'{API_VERSION}/redoc/',
        TemplateView.as_view(template_name='api/redoc.html'),
        name='redoc',
    ),
    path(
        f'{API_VERSION}/auth/token/',
        views.TokenAccessObtainView.as_view(),
        name='token-access-obtain',
    ),
    path(
        f'{API_VERSION}/auth/signup/',
        views.UserSignUpView.as_view(),
        name='auth-signup',
    ),
    path(
        f'{API_VERSION}/users/me/',
        views.OwnAccountView.as_view(),
        name='users-me',
    ),
    path(f'{API_VERSION}/', include(router_v1.urls)),
]
