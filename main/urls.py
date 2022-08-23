from rest_framework.routers import DefaultRouter

from main.views import (
    FavorViewSet, Request_FavorViewSet,
    UserViewSet, RaitingViewSet,
    CategoryViewSet, SubcategotyViewSet
)

from django.urls import path

router = DefaultRouter()

router.register('favors', FavorViewSet, basename='favors')
router.register('users', UserViewSet, basename='users')
router.register('raitings', RaitingViewSet, basename='raitings')
router.register('categories', CategoryViewSet, basename='categories')
router.register('subcategories', SubcategotyViewSet, basename='subcategories')
# router.register('comments', CommentViewSet, basename='comments')
# router.register('request-for-favors', Request_FavorViewSet, basename='request-for-favors')

urlpatterns = [
    # path('send_mail/', SendMailViewSet.as_view()),
    path('request_favor', Request_FavorViewSet.as_view())
]


urlpatterns += router.urls
