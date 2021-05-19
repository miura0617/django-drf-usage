# brands関係のテストコードを書くファイル
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import ItemCategoryModel
from .serializers import ItemCategorySerializer

# エンドポイント
ITEMCATEGORY_URL = '/app/itemcategory/'

# ItemGategoryを作成する関数
def create_itemcategory(item_category_name):
    return ItemCategoryModel.objects.create(item_category_name=item_category_name)

# 特定のItemCategoryへのURLを作成する関数
def detail_url(item_category_id):
    return reverse('app:itemcategorymodel-detail', args=[item_category_id])

# ItemCategoryのCRUD処理のテスト
class ItemCategoryApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    # GETメソッド(1)
    # 複数のitemcategoryを取得
    def test_1_1_should_get_itemcategory(self):
        create_itemcategory(item_category_name='フルーツ')
        create_itemcategory(item_category_name='野菜')
        res = self.client.get(ITEMCATEGORY_URL)

        itemcategories = ItemCategoryModel.objects.all().order_by('id')
        serializer = ItemCategorySerializer(itemcategories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    # GETメソッド(2)
    # 特定のitemcategoryを取得
    def test_1_2_should_get_single_itemcategory(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        # 特定のitemcategoryへのURLを取得(「/app/itemcategory/1/」)
        url = detail_url(itemcategory.id)
        res = self.client.get(url)
        serializer = ItemCategorySerializer(itemcategory)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    # POSTメソッド(1)
    # 新規でitemcategoryを作成
    def test_1_3_should_create_new_itemcategory(self):
        payload = {'item_category_name': 'フルーツ'}
        res = self.client.post(ITEMCATEGORY_URL, payload)

        exists = ItemCategoryModel.objects.filter(
            item_category_name = payload['item_category_name']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    # POSTメソッド(2)
    # 空のitem_category_nameを渡すと、Bad Requestが返ってくる
    def test_1_4_should_not_create_new_itemcategory_with_invalid(self):
        payload = {'item_category_name': ''}
        res = self.client.post(ITEMCATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    # PATCHメソッド
    def test_1_5_should_partial_update_itemcategory(self):
        # PATCHメソッドをテストするため、既存のbrandを作成しておく
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        payload = {'item_category_name': '野菜'}
        url = detail_url(itemcategory.id)
        self.client.patch(url, payload)
        itemcategory.refresh_from_db()

        self.assertEqual(itemcategory.item_category_name, payload['item_category_name'])

    # PUTメソッド
    def test_1_6_should_update_itemcategory(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        payload = {'item_category_name': '野菜'}
        url = detail_url(itemcategory.id)
        self.client.put(url, payload)
        itemcategory.refresh_from_db()

        self.assertEqual(itemcategory.item_category_name, payload['item_category_name'])

    # Deleteメソッド
    def test_1_7_should_delete_itemcategory(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        self.assertEqual(1, ItemCategoryModel.objects.count())

        url = detail_url(itemcategory.id)
        self.client.delete(url)        
        self.assertEqual(0, ItemCategoryModel.objects.count())

