from django import forms
from .models import Servers, ClientList, SystemCommonConfig


class ServersForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = [
            "server_name",
            "configuration_dir",
            "configuration_file",
            "status_file",
            "log_file_dir",
            "log_file",
            "startup_type",
            "startup_service",
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


# Not in use
class ClientListForm(forms.ModelForm):
    class Meta:
        model = ClientList
        fields = [
            "server",
            "cn",
            "ip",
            "toggle_time",
            "enabled",
            "status",
            "expire_date",
        ]
        widgets = {
          'comment': forms.Textarea(attrs={'rows': 2}),
        }
        
        
# Nor in use
class SystemCommonConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SystemCommonConfigForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs['readonly'] = True
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = SystemCommonConfig
        exclude = [id,]
