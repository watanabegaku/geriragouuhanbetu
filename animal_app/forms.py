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
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'username'
        self.fields['password'].widget.attrs['id'] = 'password'

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'username'
        self.fields['password1'].widget.attrs['id'] = 'password1'
        self.fields['password2'].widget.attrs['id'] = 'password2'

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')