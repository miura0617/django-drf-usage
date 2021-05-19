from rest_framework import serializers
from .models import ItemModel, ItemCategoryModel

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategoryModel
        fields = ['id', 'item_category_name']

class ItemSerializer(serializers.ModelSerializer):
    item_category_name = serializers.ReadOnlyField(
        source='item_category_id.item_category_name', 
        read_only=True)

    class Meta:
        model = ItemModel
        fields = ['id', 'item_name', 'item_category_id', 'item_category_name']
