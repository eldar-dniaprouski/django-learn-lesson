from django.contrib import admin
from . import models

# Register your models here.

# admin.site.register(models.Material)


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'material_type', 'status', 'publish')
    list_filter = ('status', 'created', 'publish', 'material_type')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created',)
    list_filter = ('created', )
    search_fields = ('name', 'email', 'body')
