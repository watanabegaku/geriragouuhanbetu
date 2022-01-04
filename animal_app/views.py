# djangoで扱うものをインポート
from django.shortcuts import render, redirect
from .models  import ModelAnimal, ModelFile
from .forms import FormAnimal, LoginForm, SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate 

# 前処理や推論で必要なものをインポート
import numpy as np
import pandas as pd
from PIL import Image
import csv
from django.http import request

## PyTorchで必要なモジュール
import torch
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from model import predict

@login_required
def classify(request):
  animals_info = list(ModelAnimal.objects.all())
  # もしanimals_info が空ならば animal_data2.csv をモデルに保存
  if not animals_info:
    with open('static/data/animal_data.csv', encoding='utf-8') as f:
      csv_data = csv.reader(f)
      # csvデータをdataリストに保存
      data = []
      # 要素番号を動物ラベルとし、アニマル豆知識データをモデルに保存
      for i, data in enumerate(csv_data):
        name, title, disc = data
        animal_info = ModelAnimal(animal_label=i, animal_name=name, animal_title=title, animal_disc=disc)
        animal_info.save()

  # もしリクエストがPOSTじゃなかったらindex.htmlを返す
  if not request.method == 'POST':
    form = FormAnimal()
    return render(request, 'index.html', {'form':form})
  # もしリクエストがPOSTであればフォーム内容を保存
  else:
    form = FormAnimal(request.POST, request.FILES)
    if form.is_valid():
      form.save()

    # リクエストのファイル名を保存し、PATHを取得
    img_name = request.FILES['image']
    img_url = 'media/documents/{}'.format(img_name)
    image_pil_mode = Image.open(img_url)
    image = np.array(image_pil_mode, dtype='uint8')
    x = predict.transform(image)
    x = x.unsqueeze(0)
    device = torch.device('cpu')
    # モデルのインスタンス化（モジュール名.クラス名）
    net = predict.Net()
    net = net.to(device)

    # パラメーターの読み込み
    net.load_state_dict(torch.load('model/animal_model.pt', map_location=device))
    net.eval()

    # 推論、予測値の計算
    y = net(x)
    # 予測ラベル
    y_arg = y.argmax()
    # detach()」はTensor型から勾配情報を抜いたものを取得する.これでndarrayに変換
    y_arg = y_arg.detach().clone().numpy()
    # 確率に変換
    y_proba = F.softmax(y, dim=1)
    # .max()で最大値を取得
    y_proba = y_proba.max() * 100
    # tensor=>numpy型に変換
    y_proba = y_proba.detach().clone().numpy()
    # 小数点第2位まで切り捨て
    y_proba = np.round(y_proba, 2)
    animal_info = ModelAnimal.objects.filter(animal_label = y_arg)
    # Queryset~となっているものの先頭を取得
  return render(request, 'classify.html', {'img_url': img_url, 'animal_info': animal_info[0], 'y_proba': y_proba, 'y_arg':y_arg})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

# ログアウトページ
class Logout(LogoutView):
    template_name = 'index.html'

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    print(form)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      new_user = authenticate(username=username, password=password)
      if new_user is not None:
        login(request, new_user)
        return render(request, 'index.html',{'form':form})
  else:
    form = SignUpForm()
    return render(request, 'index.html',{'form':form})