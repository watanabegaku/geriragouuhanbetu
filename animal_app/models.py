from django.db import models
from django.utils import timezone


class ModelAnimal(models.Model):
    id = models.AutoField(primary_key=True)
    animal_label = models.IntegerField() # 推論結果によって動物データを呼び出せるよう、動物ラベルを指定
    animal_name = models.CharField(max_length=50)
    animal_title = models.CharField(max_length=300)
    animal_disc = models.TextField()

# 画像ファイル送信用 フォームモデルの作成
class ModelFile(models.Model):
    # ImageFieldは画像を扱うことに特化したFileFieldの派生フィールド
    # Imagefield:登録時のバリデーションで画像ファイルのチェック
    # 管理用のフィールドを事前に用意すると、登録時に画像の高さと幅(pixel単位)を取得して保存
    image = models.ImageField(upload_to='documents/') # media/documentsに画像が保存される
    created_datetime = models.DateTimeField(auto_now_add=True)

# 管理画面表示用
def __str__(self):
    return (self.animal_label, self.animal_name, self.animal_title, self.animal_disc)