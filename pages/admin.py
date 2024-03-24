from django.contrib import admin

from .models import *


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("url", "user", "title", "category", "notes", "created_at")
    search_fields = ("title", "description", "summary", "notes")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "approved")
    search_fields = ("name", "description")


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Category, CategoryAdmin)