from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from twitter_clone.models import Post


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
    
    def is_valid(self):
        form = super(CreateUserForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
        
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        exclude = ('followers',)
        

class AuthenticateForm(AuthenticationForm):
    
    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
        

class PostForm(forms.ModelForm):

    def is_valid(self):
        form = super(PostForm, self).is_valid()
        for f in self.errors.iterkeys():
            self.fields[f].widget.attrs.update({'class': 'there was error'})
        return form
    
    class Meta:
        model = Post
        exclude = ('poster', 'date', )