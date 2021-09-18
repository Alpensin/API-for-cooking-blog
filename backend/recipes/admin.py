from django.contrib import admin

from .models import Follow, Ingredient, IngredientForRecipe, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("measurement_unit",)
    empty_value_display = "-пусто-"


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientForRecipeInline,)
    list_display = (
        "name",
        "author",
        "text",
        "cooking_time",
        "slug",
    )
    search_fields = ("name", "author", "text", "slug")
    list_filter = ("name", "author", "ingredients", "tags", "slug")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    search_fields = ("user", "author")
    list_filter = ("user", "author")
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
