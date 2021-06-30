from django.forms import ModelForm

from Apps.todoApp.models import Todo


class TodoForm(ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'status']
