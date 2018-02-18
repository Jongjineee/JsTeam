from django.contrib.auth.models import User
from django import forms
from .models import Photo, Profile, Comment


class UploadForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    class Meta:
        model = Photo
        exclude = ('thumnail_image', 'owner')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    class Meta :
        model = Profile
        fields = ['nickname', 'profile_photo']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message',]
        widgets = {
            'message': forms.TextInput(
                attrs={
                    'class': 'message',
                    'placeholder': '댓글 달기...',
                }
            )
        }

    def clean_content(self):
        data = self.cleaned_data['message']
        errors = []
        if data == '':
            errors.append(forms.ValidationError('댓글 내용을 입력해주세요'))
        elif len(data) > 50:
            errors.append(forms.ValidationError('댓글 내용은 50자 이하로 입력해주세요'))
        if errors:
            raise forms.ValidationError(errors)
        return data