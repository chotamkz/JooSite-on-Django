from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form

from Joo.models import Post, Comment


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'name': 'username',
            'type': 'text',
            'placeholder': 'Name'
        })
        self.fields["email"].widget.attrs.update({
            'name': 'email',
            'placeholder': 'Email'
        })
        self.fields["password1"].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields["password2"].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class PostForm(ModelForm):
    class Meta:
        managed = True
        model = Post
        fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        managed = True
        model = Comment
        fields = '__all__'


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        managed = True
        fields = ['username', 'first_name', 'last_name',  'email', 'last_login']


class UserForms(forms.ModelForm):
    class Meta:
        managed = True
        model = User
        fields = '__all__'
