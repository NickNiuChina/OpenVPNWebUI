from django import forms
from .models import Servers


class ServersForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = [
            "server_name",
            "configuration_dir",
            "startup_type",
            "service_cmd",
            "certs_dir",
            "learn_address_script",
            "managed",
            "comment"
        ]
        widgets = {
          'comment': forms.Textarea(attrs={'rows': 2}),
        }
