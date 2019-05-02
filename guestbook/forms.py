from django import forms
from .models import Comment

class TodoForm(forms.Form):
    your_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter text', 'aria-label': 'Todo', 'aria-describedby': 'add_btn'}))


class NewTodoForm(forms.ModelForm):
	class Meta:
		model = Comment

		fields = { 'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter text', 'aria-label': 'Todo', 'aria-describedby': 'add_btn'})}
		