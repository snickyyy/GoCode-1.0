from django import forms
from django.http import HttpResponse
from django_ace import AceWidget

from problems.models import Solutions


class EditorForm(forms.Form):
    text = forms.CharField(widget=AceWidget(mode="python", theme="monokai", fontsize="13px", toolbar=False))

    def clean_code(self):
        code = self.cleaned_data['text']
        print("\n\n\n\nvalidation....\n\n\n\n\n")
        # Пример проверки на запрещенные слова
        if "os" in code:
            raise forms.ValidationError("Использование 'import os' запрещено!")

        return code
