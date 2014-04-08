from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from twitter_clone.models import Post, User


class CreateUserForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': ("A user with that email already exists."),
        'password_mismatch':("Those two passwords don't match."),
        }
    
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label=("Password Confirmation"), widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
        
    class Meta:
        model = User
        fields = ("email",)
        exclude = ('followers',)
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_message['duplicate username'])
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2
        
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        

class AuthenticateForm(AuthenticationForm):
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
      

class PostForm(forms.ModelForm):

    def is_valid(self):
        form = super(PostForm, self).is_valid()
        for f in self.errors.iterkeys():
            self.fields[f].widget.attrs.update({'class': 'there was error'})
        return form
    
    class Meta:
        model = Post
        exclude = ('poster', 'date', )