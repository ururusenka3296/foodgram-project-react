from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (Favourites, IngredientViewSet, RecipeViewSet,
                    Shopping_listViews, Subscribe, SubscriptionsViews,
                    TagViewSet)


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        Shopping_listViews.as_view(),
        name='shopping_cart'),
    path(
        'recipes/<int:recipe_id>/favorite/',
        Favourites.as_view(),
        name='favourites'),
    path(
        'users/<int:user_id>/subscribe/',
        Subscribe.as_view(),
        name='subscribe'),
    path(
        'users/subscriptions/',
        SubscriptionsViews.as_view(),
        name='subscriptions'),

    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
