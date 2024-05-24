from django import forms
from app.models import *
from django.contrib.auth import authenticate, login

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        #super().clean()
        user = authenticate(**self.cleaned_data)
        if not user:
            raise forms.ValidationError("Incorrect username or/and password")

class SignupForm(forms.ModelForm):
    username = forms.CharField()
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise forms.ValidationError('Password don\'t match!')
        
    
    def save(self, commit=True):
        """ user=User(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        user.save() """
        user=User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        profile = Profile(user=user, name=self.cleaned_data['name'], avatar=self.cleaned_data['avatar'])
        profile.save()
        user.save()

        return user
    
    class Meta:
        model = Profile
        fields = ['username', 'name', 'password', 'repeat_password', 'avatar']

class SettingsForm(forms.Form):
    new_username = forms.CharField()
    new_name = forms.CharField()
    new_password = forms.CharField(widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput)
    new_avatar = forms.ImageField(required=False)

    def clean(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['repeat_new_password']:
            raise forms.ValidationError('Password don\'t match!')
        if User.objects.filter(username=self.cleaned_data['new_username']).count() > 0:
            raise forms.ValidationError('Username exists')
    
    def save(self, user, commit=True):
        user.username=self.cleaned_data['new_username']
        user.set_password(self.cleaned_data['new_password'])
        user.save()
        profile=Profile.objects.get(user=user)
        profile.name=self.cleaned_data['new_name']
        if self.cleaned_data['new_avatar']:
            profile.avatar.delete(save=True)
            profile.avatar=self.cleaned_data['new_avatar']
        profile.save()

    
    class Meta:
        model = Profile
        fields = ['user', 'name', 'avatar', 'password']

class AskForm(forms.ModelForm):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()

    def save(self, user, commit=True):
        author=Profile.objects.get(user=user)
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'], author=author)
        question.save()
        tags = [tag.strip() for tag in self.cleaned_data['tags'].split(',')]
        for tag in tags:
            if len(Tag.objects.filter(name=tag)) == 0:
                new_tag=Tag(name=tag)
                new_tag.save()
            question.tag.add(Tag.objects.get(name=tag))

        return question

    class Meta:
        model = Question
        fields=['title', 'text']

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    def save(self, question, user, commit=True):
        answer = Answer(text=self.cleaned_data['text'], author=Profile.objects.get(user=user), question=question)
        answer.save()

    class Meta:
        model = Answer
        fields=['text']

