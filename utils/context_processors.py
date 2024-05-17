from django.conf import settings
from ovpn.models import Servers


def get_version_number(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {'APP_VERSION_NUMBER': settings.APP_VERSION_NUMBER}


def get_openvpn_servers(request):
    servers = Servers.objects.filter(managed=1)
    openvpn_server_list = {}
    if servers:
        for server in servers:
            openvpn_server_list.update({server.server_name: str(server.id)})
    return {'OPENVPN_SERVER_LIST': openvpn_server_list}
