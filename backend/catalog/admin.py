from django.contrib import admin

from .models import Category, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("display_name", "slug", "order")
    search_fields = ("display_name", "slug")
    ordering = ("order",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "premiered", "genres")
    search_fields = ("name", "overview")
    list_filter = ("categories",)
    filter_horizontal = ("categories",)
