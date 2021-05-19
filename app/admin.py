from django.contrib import admin
from .models import ItemModel, ItemCategoryModel

# Register your models here.

admin.site.register(ItemCategoryModel)
admin.site.register(ItemModel)
