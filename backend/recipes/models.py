from enum import unique

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from .utils import slugify

User = get_user_model()


class Tag(models.Model):
    """Tags model"""

    name = models.CharField(
        verbose_name="название", max_length=250, unique=True
    )
    color = ColorField(default="#FF0000", unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    @property
    def css_style(self):
        return f"badge_style_{self.badge_style}"


class Ingredient(models.Model):
    """Model for ingredients"""

    name = models.CharField(
        verbose_name="название ингредиента", max_length=128
    )
    measurement_unit = models.CharField(
        verbose_name="единица измерения", max_length=128
    )

    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        indexes = [models.Index(fields=["name"])]
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Model for recipes"""

    name = models.CharField(verbose_name="название рецепта", max_length=128)
    author = models.ForeignKey(
        User,
        verbose_name="автор",
        on_delete=models.CASCADE,
        related_name="written_recipes",
    )
    image = models.ImageField(
        verbose_name="изображение", upload_to="recipe_images/"
    )
    text = models.TextField(verbose_name="текстовое описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="ингредиенты",
        related_name="recipes",
        through="IngredientForRecipe",
        through_fields=("recipe", "ingredient"),
    )
    in_favorites = models.ManyToManyField(
        User,
        verbose_name="в избранном",
        related_name="followed_recipes",
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="тэги",
        related_name="recipes",
    )
    cooking_time = models.DecimalField(
        verbose_name="время приготовления",
        max_digits=4,
        decimal_places=1,
        validators=(MinValueValidator(0.1),),
    )
    slug = models.SlugField("slug", unique=True)

    pub_date = models.DateTimeField(
        verbose_name="дата создания", auto_now_add=True
    )

    class Meta:
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["pub_date"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "author"], name="unique_name_for_author"
            ),
        ]
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug
        super().save(*args, **kwargs)


class IngredientForRecipe(models.Model):
    """Model for setting ingredients to recipe"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="рецепт",
        related_name="ingredientsforrecipe",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="ингредиент",
        related_name="ingredientsforrecipe",
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(
        verbose_name="количество",
        max_digits=6,
        decimal_places=1,
        validators=(MinValueValidator(1),),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("ingredient", "recipe"), name="unique_ingr_recipe"
            )
        ]
        db_table = "foodgram_ingr_for_recipe"

    def __str__(self):
        return f"{self.recipe}: {self.ingredient}"


class Follow(models.Model):
    """Follow model to subscribe on some author"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписанный",
        help_text="Выберите пользователя",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор для подписки",
        help_text="Выберите автора",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "author"), name="unique_following"
            )
        ]

    def __str__(self):
        return f"Подписка {self.user} на {self.author}"
