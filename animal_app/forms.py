from django import forms
from .models import ModelFile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm # 追加
from django.contrib.auth.models import User # 追加

# モデルからフォームを作成
class FormAnimal(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control-file'
            field.widget.attrs['id'] = 'image-input'
    class Meta:
        model = ModelFile # 画像ファイル送信用 フォームモデル
        fields = ('image',) # form 項目には画像を指定 , が無いとerror

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #htmlの表示を変更可能にします
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')