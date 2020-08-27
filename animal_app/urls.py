from django.urls import path
from . import views
from django.conf import settings #追加
from django.conf.urls.static import static #追加

urlpatterns = [
  path('', views.classify, name='classify'),
  path('login/', views.Login.as_view(), name='login'),
  path('logout/', views.Logout.as_view(), name='logout'),
  path('signup', views.signup, name='signup'),
]

# mediaディレクトリの画像表示のため
# 画像はlocalなStorageのMEDIA_ROOTに保存され、localなurl(相対url)のMEDIA_URLで参照
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)