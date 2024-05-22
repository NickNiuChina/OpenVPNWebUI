from django import forms
from .models import Servers


class ServersForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = [
            "server_name",
            "configuration_dir",
            "configuration_file",
            "status_file",
            "log_file",
            "startup_type",
            "service_cmd",
            "certs_dir",
            "learn_address_script",
            "managed",
            "management_port",
            "management_password",
            "comment"
        ]
        widgets = {
          'comment': forms.Textarea(attrs={'rows': 2}),
        }
