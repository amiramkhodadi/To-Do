from django.contrib import admin

from .models import TODOO


@admin.register(TODOO)
class TODOOAdmin(admin.ModelAdmin):
    list_display = ("srno", "title", "user", "status", "date")
    list_filter = ("status", "date")
    search_fields = ("title", "user__username")
    readonly_fields = ("date",)
    list_select_related = ("user",)
