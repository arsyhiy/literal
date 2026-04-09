from django.contrib import admin
from .models import (
    Category,
    Product,
    Book,
    BoardGame,
    Publisher,
    Author,
    Order,
    OrderItem,
)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "numberOfPages", "category", "price")
    search_fields = ("name", "author")
    list_filter = ("category",)


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ("name", "players", "timeOfPlaying", "category", "price")
    search_fields = ("name",)
    list_filter = ("category",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "total", "created_at")
    inlines = [OrderItemInline]
