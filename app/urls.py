from django.urls import path, include
# DRFのrouterを使う
from rest_framework.routers import DefaultRouter
# Viewのインポート
from . import views

app_name = 'app'

# DefaultRouter設定
router = DefaultRouter()
router.register('itemcategory', views.ItemCategoryViewSet)
router.register('item', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
