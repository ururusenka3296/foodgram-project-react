from django.contrib import admin

from .models import (Favourites, Ingredient, RecipeIngredient, Recipe,
                     Shopping_list, Tag)
from .forms import IngredientForm


class IngredientInRecipeInLime(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    formset = IngredientForm


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'image',
                    'text', 'cooking_time', 'get_followers_count')
    empty_value_display = '-пусто-'
    search_fields = ('name', )
    list_filter = ('author', )
    empty_value_display = '-пусто-'
    ordering = ['name']
    inlines = (IngredientInRecipeInLime, )

    @admin.display(description='Добавили в избранное')
    def get_followers_count(self, obj):
        return obj.favourites.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    ordering = ['name']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    ordering = ['name']


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
    ordering = ['user']


class Shopping_listAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
    ordering = ['user']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(Shopping_list, Shopping_listAdmin)
