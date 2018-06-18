from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows': 5, 'placeholder': 'What you curious about?'}
		), 
		max_length=4000,
		help_text='<ul><li>Max length is 4000</li><li>Two spaces adds new line</li></ul>'
	)

	class Meta:
		model = Topic
		fields = ('name', 'message')


class NewPostForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows': 5, 'placeholder': 'Do you know the way?'}
		), 
		max_length=4000,
		help_text='<ul><li>Max length is 4000</li><li>Two spaces adds new line</li></ul>'
	)

	class Meta:
		model = Post
		fields = ('message',)