# テストコードを書くファイル
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import ItemCategoryModel, ItemModel
from .serializers import ItemSerializer
from decimal import Decimal

# エンドポイントをあらかじめ定義しておく
ITEMCATEGORY_URL = '/app/itemcategory/'
ITEM_URL = '/app/item/'

# ItemGategoryを作成する関数
def create_itemcategory(item_category_name):
    return ItemCategoryModel.objects.create(item_category_name=item_category_name)

# itemを作成する関数
def create_item(**params):
    defaults = {
        'item_name': 'りんご',
    }
    defaults.update(params)

    return ItemModel.objects.create(**defaults)


# 特定のItemCategoryへのURLを作成する関数
def detail_itemcategory_url(item_category_id):
    return reverse('app:itemcategorymodel-detail', args=[item_category_id])

# 特定のItemへのURLを作成する関数
def detail_item_url(vehicle_id):
    return reverse('app:itemmodel-detail', args=[vehicle_id])


# ItemのCRUD処理のテスト
class ItemApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    # GETメソッド(1)
    # item一覧を取得できるか確認
    def test_2_1_should_get_item(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        create_item(item_name='りんご', item_category_id=itemcategory)
        create_item(item_name='みかん', item_category_id=itemcategory)

        res = self.client.get(ITEM_URL)
        items = ItemModel.objects.all().order_by('id')
        serializer = ItemSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # GETメソッド(2)
    # 特定のitemを取得
    def test_2_2_should_get_single_item(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        item = create_item(item_name='りんご', item_category_id=itemcategory)
        url = detail_item_url(item.id)
        res = self.client.get(url)
        serializer = ItemSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # POSTメソッド(1)
    # 新規でitemを作成
    def test_2_3_should_create_new_item_successfully(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        payload = {
            'item_name': 'みかん',
            'item_category_id': itemcategory.id,
        }
        res = self.client.post(ITEM_URL, payload)
        # DBのデータ取得
        item = ItemModel.objects.get(id=res.data['id'])
        # status code確認
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # DB内容とpayloadで渡したparamsが一致するか確認
        self.assertEqual(payload['item_name'], item.item_name)
        self.assertEqual(payload['item_category_id'], item.item_category_id.id)
    
    # POSTメソッド(2)
    # 空のitem_category_idを渡すと、Bad Requestが返ってくる
    def test_2_4_should_not_create_item_with_invalid(self):
        payload = {
            'item_name': 'みかん',
            'item_category_id': '',
        }
        res = self.client.post(ITEM_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Patchメソッド
    def test_2_5_should_partial_update_item(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        item = create_item(item_name='りんご', item_category_id=itemcategory)
        # PATCHの場合は変更対象の属性をpayloadで指定するだけでよい
        payload = {'item_name': 'みかん'}
        url = detail_item_url(item.id)
        self.client.patch(url, payload)
        item.refresh_from_db()
        self.assertEqual(item.item_name, payload['item_name'])

    # PUTメソッド
    def test_2_6_should_update_item(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        item = create_item(item_name='りんご', item_category_id=itemcategory)
        # PUTの場合は全属性をpayloadで指定する必要あり
        payload = {
            'item_name': 'みかん',
            'item_category_id': itemcategory.id,
        }
        url = detail_item_url(item.id)
        self.assertEqual(item.item_name, 'りんご')

        self.client.put(url, payload)
        item.refresh_from_db()
        self.assertEqual(item.item_name, payload['item_name'])
    

    # Deleteメソッド
    def test_2_7_should_delete_item(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        item = create_item(item_name='りんご', item_category_id=itemcategory)
        self.assertEqual(1, ItemModel.objects.count())

        url = detail_item_url(item.id)
        self.client.delete(url)
        self.assertEqual(0, ItemModel.objects.count())

    # Deleteメソッド：CASCADE
    def test_2_8_should_cascade_delete_item_by_itemcategory_delete(self):
        itemcategory = create_itemcategory(item_category_name='フルーツ')
        item = create_item(item_name='りんご', item_category_id=itemcategory)
        self.assertEqual(1, ItemModel.objects.count())

        # itemcategoryのURL取得し、itemcategoryを削除
        url = detail_itemcategory_url(itemcategory.id)
        self.client.delete(url)
        self.assertEqual(0, ItemModel.objects.count())

