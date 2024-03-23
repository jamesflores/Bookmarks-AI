from django.contrib import admin

from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "url", "note", "created_at")
    search_fields = ("url", "note")


admin.site.register(Bookmark, BookmarkAdmin)
