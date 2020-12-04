from .models import *
from django.forms import ModelForm


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        exclude = ['entry_author']
