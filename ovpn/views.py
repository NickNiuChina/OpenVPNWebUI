import subprocess

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servers, ClientList
from users.models import User, UserGroup
import platform
import datetime
from .forms import ServersForm
import uuid
import psutil
import time
import pathlib
from utils.OpenVPNParser import OpenVPNParser
from utils.LogParser import LogParser
from django.db.models import Q, CharField, Value


def index(request):
    """ Dashboard

    Args:
        request (django.http.request): django request object 

    Returns:
        template: template main.html with context of system informations
    """
    system_type = platform.system()
    system_info = {
        "system_type": system_type,
        "system_version": platform.release(),
        "system_time": datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
        "cpu_cores": psutil.cpu_count(),
    }

    boot_time_timestamp = psutil.boot_time()
    current_time_timestamp = time.time()
    uptime_seconds = current_time_timestamp - boot_time_timestamp
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_str = f"{int(uptime_days)} days,{int(uptime_hours % 24)}:{int(uptime_minutes % 60)}:{int(uptime_seconds % 60)}"

    load_avg = psutil.getloadavg()
    memory_total = round(psutil.virtual_memory().total/1024/1024, 1)
    memory_used = round(psutil.virtual_memory().used/1024/1024, 1)
    memory_percent = psutil.virtual_memory().percent
    swap_total = round(psutil.swap_memory().total/1024/1024, 1)
    swap_used = round(psutil.swap_memory().used/1024/1024, 1)
    swap_percent = round(psutil.swap_memory().percent/1024/1024, 1)

    if system_type.startswith("Linux"):
        openvpn_version = OpenVPNParser.get_openvpn_version()
    else:
        openvpn_version = "NA"
    system_information = platform.platform()

    system_info.update(
        {
            "system_uptime": uptime_str,
            "load_avg": load_avg,
            "memory_total": memory_total,
            "memory_used": memory_used,
            "memory_percent": memory_percent,
            "swap_total": swap_total,
            "swap_used": swap_used,
            "swap_percent": swap_percent,
            "openvpn_version": openvpn_version,
            "system_information": system_information
        }
    )
    context = {'system_info': system_info}
    if request.method == "POST":
        if request.POST.get('action', '') == "db_refresh":
            return JsonResponse(context)
    return render(request, 'ovpn/main.html', context)


def servers(request):
    """ Openvpn server list or post to add new server

    Args:
        request (django.http.request): django.http.request

    Returns:
        template: template ovpn/servers.html with context {servers, form}
    """
    servers = Servers.objects.all()
    return_servers = []
    for server in servers:
        if not platform.system().startswith("Linux"):
            server.running_status = 0
        else:            
            status = OpenVPNParser.get_openvpn_running_status(server)
            if status:
                server.running_status = status["status"]
            else:
                server.running_status = 0
        return_servers.append(server)
    form = ServersForm()    
    if request.method == "POST":
        formset = ServersForm(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "New server has been added successfully!")
        else:
            messages.error(request, formset.errors)
        form = ServersForm()
        return render(request, 'ovpn/servers.html', {"servers": servers, "form": form})
    else:
        return render(request, 'ovpn/servers.html', {"servers": return_servers, "form": form})


def server_delete(request):
    """ Post to delete an Openvpn server

    Args:
        request (django.http.request): 
        uuid: openvpn service id

    Returns:
        redirect: redirect("ovpn:servers")
    """
    if request.method != 'POST':
        return HttpResponse("Page not found", status=404)
    else:
        service_uuid = request.POST.get('service_uuid').strip()
        if uuid:
            try:
                sid = uuid.UUID(service_uuid)
            except:
                sid = ''
            if sid:
                server = Servers.objects.filter(id=sid)
                if not server:
                    messages.error(request, "This uuid is found in record!")
                    return redirect("ovpn:servers")
                else:
                    Servers.objects.filter(id=sid).delete()
                    messages.success(request, "OpenVPN deleted successfully!")
                    return redirect("ovpn:servers")
            else:
                messages.error(request, "Please provide a valid uuid!")
                return redirect("ovpn:servers")
        else:
            messages.error(request, "UUID is required for this request")
            return redirect("ovpn:servers")


def server_update(request, sid):
    """ OpenVPN server update

    Args:
        request (_type_): _description_
        sid (_type_): _description_

    Returns:
        _type_: _description_
    """
    server = get_object_or_404(Servers, id=sid)

    if request.method == 'GET':
        context = {'form': ServersForm(instance=server), 'id': sid}
        return render(request, 'ovpn/server_update.html', context)

    elif request.method == 'POST':
        form = ServersForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            messages.success(request, 'The service has been updated successfully.')
            return redirect('ovpn:servers')
        else:
            messages.error(request, 'Please correct the following errors: ' + str(form.errors))
            context = {'form': ServersForm(instance=server), 'id': sid}
            return render(request, 'ovpn/server_update.html', context)


def server_logs(request, ovpn_service=None):
    """_summary_

    Args:
        request (_type_): _description_
        ovpn_service (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    ovpn_service = get_object_or_404(Servers, server_name=ovpn_service)
    context = {}
    ovpn_logs = []
    # ovpn_service = Servers.objects.filter(server_name=ovpn_service).first()
    context.update({"server": ovpn_service})
   
    if platform.system().startswith("Linux"):
        logs_file_dir = pathlib.Path(ovpn_service.log_file_dir)
        if logs_file_dir.exists():
            for f in list(logs_file_dir.iterdir()):
                if f.is_file() and f.name.endswith(".log"):
                    ovpn_logs.append({"log_name": f.name, "log_size": round(f.stat().st_size/1024, 1)})
            if not ovpn_logs:
                messages.error(request, "No OpenVPN logfiles found!")
                return render(request, 'ovpn/server_logs.html', context)
            else:
                context.update({"ovpn_logs": ovpn_logs})
                return render(request, 'ovpn/server_logs.html', context)
        else:
            messages.error(request, "The OpenVPN logs file dir do not exist!")
            return render(request, 'ovpn/server_logs.html', context)
    else:
        messages.error(request, "This APP should run on linux debian platform!:")
        return render(request, 'ovpn/server_logs.html', context)


def server_log(request, ovpn_service=None, log_file=None):
    """_summary_

    Args:
        request (_type_): _description_
        ovpn_service (_type_, optional): _description_. Defaults to None.
        log_file (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    ovpn_service = get_object_or_404(Servers, server_name=ovpn_service)
    authenticated = request.session.get("authenticated")
    user_id = authenticated['id']
    user = User.objects.get(id=user_id)
    # print(user.log_size)
    
    # form to update 
    if request.method == "POST":
        new_size = int(request.POST.get("log_size"))
        if user.log_size == new_size:
            messages.warning(request, "You did not submit a new value!")
        else:
            user.log_size = new_size
            user.save()
            messages.success(request, "Log lines has been update successfully!")
        return redirect('ovpn:server_log', ovpn_service=ovpn_service.server_name, log_file=log_file)
    
    context = {}
    
    logs_file_dir = pathlib.Path(ovpn_service.log_file_dir, log_file)
    log_size = int(user.log_size)
    context.update({"log_size": log_size, "ovpn_service": ovpn_service, "log_file": log_file})
    if logs_file_dir.is_file():
        log_content = LogParser.read_log(log_size, logs_file_dir)
        context.update({"log_content": log_content})
    else:
        messages.error(request, "Logfile does not exist!")
    return render(request, 'ovpn/server_log.html', context)


def clients(request, ovpn_service=None):
    """ OpenPVN client page also accept POST request

    Args:
        request (django.http.request): django.http.request
        ovpn_service (str, optional): the openvpn service name. Defaults to None will return 404.
        action (str, ["list", "update_site_name"]):
            "list": this request from ajax to retrieve client list
            "update_site_name": from client page to update site_name

    Returns:
        JsonResponse: this response to ajax
        redirect: redirect client page for post request
        tempate: get request and return template
    """
    ovpn_server = Servers.objects.get(server_name=ovpn_service)
    clients = ClientList.objects.filter(server=ovpn_server)
    authenticated = request.session.get("authenticated")
    user_id = authenticated['id']
    user = User.objects.get(id=user_id)   
    group = user.group.name
    context = {"clients": clients, "server": ovpn_server, "user": user}

    if request.method == "POST":
        # return json to datatables
        if request.POST.get('action', '') == "list":
            draw = request.POST.get('draw')
            start = request.POST.get('start')
            length = request.POST.get('length')
            searchValue = request.POST.get('search[value]')
            order_col = request.POST.get("order[0][column]")
            order_direction = request.POST.get("order[0][dir]")
            # print(draw, start, length, searchValue, order_col, order_direction)
            # 7 0 50  0 asc
            
            results = ClientList.objects.filter(server=ovpn_server)
            recordsTotal = len(results)
            if searchValue and searchValue.strip():
                query = searchValue.strip()
                lookups= Q(id__icontains=query) | Q(site_name__icontains=query) | Q(cn__icontains=query) | Q(ip__icontains=query)
                # results =results.filter(lookups).distinct()
                results =ClientList.objects.annotate(foo=Value(query, CharField())).filter(lookups).distinct()
                recordsFiltered = len(results)
            else:
                results = results
                recordsFiltered = len(results)

            columns = ['id', 'site_name', 'cn', 'ip', "toggle_time", "status"]
            col = columns[int(order_col)]
            if order_direction == "asc":
                results = results.order_by(col)[int(start):int(length)]
            else:
                results = results.order_by('-' + col)[int(start):int(length)]
                       
            data = {
                'recordsFiltered': recordsFiltered,
                'recordsTotal': recordsTotal,
                'draw': draw,
                'data': [ d for d in results.values() ],
                "privs_group": group,
                'pageLength': user.page_size
            }
            return JsonResponse(data)
        # operate for site name changing
        elif request.POST.get('action', '') == "update_site_name":
            client_cn = request.POST.get('client_cn', '')
            new_site_name = request.POST.get('newSiteName', '')
            site_name = ""
            if new_site_name and new_site_name.strip():
                site_name = new_site_name
            
            if site_name:
                client = ClientList.objects.filter(server=ovpn_server).get(cn=client_cn)
                if client:
                    client.site_name = site_name
                    client.save()
                    messages.success(request, "Client site_name has been updated successfully.")
                else:
                    messages.error(request, "cn is not correct!")
            else:
                messages.error(request, "Please provide a valid site name!")    
            return redirect("ovpn:clients", ovpn_service=ovpn_server.server_name)
    # get request
    else:
        return render(request, 'ovpn/clients.html', context)


def show_settings(request):
    """List Django setting values

    Args:
        request (get): django request object

    Returns:
        HttpResponse: settings key/value(s)
    """
    res = ''
    from django.conf import settings
    for name in dir(settings):
        if not name.startswith("_"):
            res += '</br>'
            res += str(name)
            res += ':'
            res += str(getattr(settings, name))
    return HttpResponse(res)


def show_sessions(request):
    """ List django session values

    Args:
        request (get): django request object

    Returns:
        HttpResponse: session key/value(s)
    """
    res = ''
    for key, value in request.session.items():
        res += '</br>'
        res += str(key)
        res += ':'
        res += str(value)
    return HttpResponse(res)