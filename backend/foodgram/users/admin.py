from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'get_count_followers',
        'get_recipes_count'
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
    ordering = ['username']

    @admin.display(description='Количество подписчиков')
    def get_count_followers(self, obj):
        return obj.follower.count()

    @admin.display(description='Количество рецептов')
    def get_recipes_count(self, obj):
        return obj.recipe.count()


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    empty_value_display = '-пусто-'
    ordering = ['user']


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
