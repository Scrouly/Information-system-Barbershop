from django import forms
from django.utils.safestring import mark_safe

class CustomClearableFileInput(forms.ClearableFileInput):
    template_with_initial = '%(input)s'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial_text': '',
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            'input': super().render(name, value, attrs, renderer),
        }

        template = '%(input)s'

        return mark_safe(template % substitutions)

