# 実行方法

## git cloneする

git clone https://github.com/miura0617/django-drf-usage.git

## フォルダ移動
cd django-drf-usage

## 仮想環境を作成し、仮想環境を有効にします

以下のコマンドで仮想環境を作成します。

python -m venv venv

以下のコマンドで仮想環境を有効にします。

venv\Scripts\activate

## 仮想環境に外部ライブラリをインストールし、開発環境を復元します

pip install -r requirements.txt

## インストールした外部ライブラリを確認

外部ライブラリにdjangoとdjangorestframeworkがあることを確認

pip freeze

## SECRET_KEYを作成します

以下のURLを元に\project\get_random_secret_key.pyを作成後、ファイルを実行してSECRET_KEYを作成します
https://qiita.com/frosty/items/bb5bc1553f452e5bb8ff


python project\get_random_secret_key.py


## project\local_settings.pyを作成し、先程作成したSECRET_KEYを定義します


## モデルを生成

以下の2つのコマンドを実行し、モデルを生成します

python manage.py makemigrations
python manage.py migrate

## スーパユーザを作成

以下のコマンドでスーパユーザを作成します。

python manage.py createsuperuser


ユーザ名、E-mail、パスワード、パスワード(再入力)をしてスーパーユーザを作成できます。


## サーバを起動します

python manage.py runserver


# 動作確認方法

## 管理画面にログインする

管理画面「http://127.0.0.1:8000/admin/」にアクセスし、スーパーユーザでログインします

## DRFのURLにアクセスします

「http://127.0.0.1:8000/app/itemcategory/」
「http://127.0.0.1:8000/app/item/」

 詳細については[こちら](https://engineer-lifestyle-blog.com/code/python/django-restframework-usage-behavior-confirmation/)の記事を参照してください。


 # テスト実行方法

python manage.py test
