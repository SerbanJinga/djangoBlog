
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model

)
from .models import Post, Comment

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'full-width',
        'placeholder': 'Username'
    }), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'full-width',
        'placeholder': 'Password'
    }), label='')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={
        'class': 'full-width',
        'placeholder': 'Enter your email*'
    }))
    email2 = forms.EmailField(label='',widget=forms.TextInput(attrs={
        'class': 'full-width',
        'placeholder': 'Enter your email again*'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'full-width',
        'placeholder': 'Enter your password*'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'full-width',
        'id': 'cMessage',
        'name': 'cMessage',
        'placeholder': 'Your Message*',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields=('content',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'header', 'after_header', 'quote', 'all_text', 'paragraph1', 'header1', 'paragraph2', 'header2', 'categories', 'tags', 'featured', 'previous_post', 'next_post')
