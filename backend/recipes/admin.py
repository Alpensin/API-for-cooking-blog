from django.contrib import admin
from django.template.loader import render_to_string
from sorl.thumbnail.admin import AdminImageMixin

from .models import Follow, Ingredient, IngredientForRecipe, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "unit")
    search_fields = ("title",)
    list_filter = ("unit",)
    empty_value_display = "-пусто-"


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe


class RecipeAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = (IngredientForRecipeInline,)
    list_display = (
        "photo",
        "title",
        "author",
        "description",
        "cooking_time",
        "slug",
    )
    search_fields = ("title", "author", "description", "slug")
    list_filter = ("title", "author", "ingredients", "tags", "slug")
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("title",)}

    def photo(self, obj):
        return render_to_string("utils/thumb.html", {"image": obj.picture})

    photo.allow_tags = True


class TagAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_filter = ("title",)
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
