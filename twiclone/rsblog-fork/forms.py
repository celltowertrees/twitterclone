from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from models import Item


class ItemForm(forms.ModelForm):
	title = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Title'}))
	content = forms.CharField(widget=forms.widgets.Textarea(attrs={'placeholder': 'Content'}))

	def is_valid(self):
		form = super(ItemForm, self).is_valid()
		for f in self.errors.iterkeys():
			self.fields[f].widget.attrs.update({'class': 'there was error'})
		return form

	class Meta:
		model = Item
		fields = ['title', 'content',]
		exclude = ['slug', 'created',]


