from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'size', 'date')
    list_filter = ('date',)
    search_fields = ('name',)
    readonly_fields = ('size', 'date')
