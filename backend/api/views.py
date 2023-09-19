from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, RecipeIngredient, Recipe, Tag
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User

from .permissions import IsAdminOrReadOnly, IsAuthororAdminorRead
from .serializers import (CreateUpdateRecipeSerializer, FavouriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer)
from .filters import IngredientFilter, RecipeFilter


class TagViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Тегов.'''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Ингредиентов.'''

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter


class Favourites(generics.RetrieveDestroyAPIView, generics.ListCreateAPIView):
    '''Вью для добавления и удаления рецепта в избранное.'''

    queryset = Recipe.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        '''Получение id рецепта из URL.'''
        return get_object_or_404(Recipe, id=self.kwargs['recipe_id'])

    def create(self, request, *args, **kwargs):
        '''Добавление в избранное.'''
        recipe = self.get_object()
        favorite = request.user.favourites.create(recipe=recipe)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        '''Удаление подписки.'''
        self.request.user.favourites.filter(recipe=instance).delete()


class RecipeViewSet(viewsets.ModelViewSet):
    '''Вьюсет для рецептов.'''

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthororAdminorRead, )

    def get_serializer_class(self):
        '''Переопределение сериализатора для POST запроса.'''
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return CreateUpdateRecipeSerializer

    def perform_create(self, serializer):
        '''Добавление автора рецепта, пользователя который сделал запрос.'''
        serializer.save(author=self.request.user)

    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredients = (RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit',).annotate(
            amount=Sum('amount')).order_by()
        )
        data = []
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount']
            data.append(f'{name}: {amount}, {measurement_unit}\n')
        response = HttpResponse(content=data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="cart.txt"'
        return response


class Subscribe(generics.RetrieveDestroyAPIView, generics.ListCreateAPIView):
    """Подписка и отписка от пользователя."""

    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        '''Получение id пользователя из URL.'''
        user_id = self.kwargs['user_id']
        return get_object_or_404(User, id=user_id)

    def get_queryset(self):
        '''Проверка наличие подписки.'''
        follow = Follow.objects.filter(
            user=self.request.user, author=self.get_object()).exists()
        return follow

    def create(self, request, *args, **kwargs):
        '''Создание подписки.'''
        user_author = self.get_object()
        if request.user.id == user_author.id:
            return Response('Нельзя подписаться на самого себя!',
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.follower.filter(author=user_author).exists():
            return Response('Нельзя подписаться дважды!',
                            status=status.HTTP_400_BAD_REQUEST)
        subscribe = request.user.follower.create(author=user_author)
        serializer = self.get_serializer(subscribe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        '''Удаление подписки.'''
        self.request.user.follower.filter(author=instance).delete()


class Shopping_listViews(generics.RetrieveDestroyAPIView,
                         generics.ListCreateAPIView):
    """Добавление и удаление рецептов из листа покупок."""

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        '''Получение id рецепта из URL.'''
        return get_object_or_404(Recipe, id=self.kwargs['recipe_id'])

    def create(self, request, *args, **kwargs):
        '''Добавление в список покупок.'''
        recipe = self.get_object()
        request.user.shopping_list.create(recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        '''Удаление рецепта из листа покупок.'''
        self.request.user.shopping_list.filter(
            recipe=self.get_object()).delete()


class SubscriptionsViews(generics.ListAPIView):
    '''Вьюсет для отображения подписок пользователя'''

    queryset = Follow.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        '''Метод для отображения всех подписок пользователя.'''
        follows = request.user.follower
        serializer = SubscribeSerializer(follows, many=True)
        return Response(serializer.data)
