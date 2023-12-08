from django.contrib import admin
from .models import *


class SubcategoryAdmin(admin.StackedInline):
    model = SubCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryAdmin,]
    list_display = ['name']
    search_fields = ['name']



