from django.forms import ModelForm

from Apps.todo.models import Todo


class TodoForm(ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'status']
