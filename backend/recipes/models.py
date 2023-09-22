from colorfield.fields import ColorField
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField('Название тега',
                            max_length=150,
                            null=False)
    color = ColorField('Цвет тега',
                       default='#ffffff',
                       null=False)
    slug = models.CharField('slug',
                            max_length=150,
                            null=False,
                            unique=True
                            )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def str(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField('Название ингредиента',
                            max_length=150
                            )
    measurement_unit = models.CharField('Единицы измерения',
                                        max_length=150
                                        )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def str(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта',
    )
    name = models.CharField('Название рецепта',
                            max_length=150
                            )
    image = models.ImageField('Фото рецепта',
                              upload_to='recipe/',
                              null=True,
                              default=None
                              )
    text = models.TextField('Описание рецепта')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField('Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ("-id",)

    def str(self):
        return self.name


class RecipeIngredient(models.Model):
    """Буферная модель для связи моделей ингредиента и рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
        blank=False,
        null=False
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингредиент',
        blank=False,
        null=False
    )
    amount = models.PositiveIntegerField(
        'Колличество ингредиента.',
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def str(self):
        return f'{self.amount}гр. {self.ingredient.name} в {self.recipe.name}'


class Favourites(models.Model):
    """Модель Избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favourites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в избранном',
        related_name='favourites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def str(self):
        return f'Пользователь {self.user} добавил в избранное {self.recipe}'


class ShoppingList(models.Model):
    """Модель листа покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в избранном',
        related_name='shopping_list'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def str(self):
        return f'Список покупок {self.user}'
