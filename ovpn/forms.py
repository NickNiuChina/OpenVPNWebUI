from django import forms
from .models import Servers


class ServersForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = [
            "server_name",
            "configuration_dir",
            "service_cmd",
            "learn_address_script",
            "managed",
            "comment"
        ]
        widgets = {
          'comment': forms.Textarea(attrs={'rows': 2}),
        }