from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
# 作成したserializerをインポート
from .serializers import ItemCategorySerializer, ItemSerializer
# 作成したモデルもインポート
from .models import ItemCategoryModel, ItemModel


# Create your views here.

class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategoryModel.objects.all()
    serializer_class = ItemCategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer


