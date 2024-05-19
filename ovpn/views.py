from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servers
import platform
import datetime
from .forms import ServersForm
import uuid
import psutil
import time


def index(request):
    system_type = platform.system()
    system_info = {
        "system_type": system_type,
        "system_version": platform.version(),
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
        openvpn_version = "NA"
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
    print(context)
    return render(request, 'ovpn/main.html', context)


def servers(request):
    servers = Servers.objects.all()
    form = ServersForm()

    if request.method == "POST":
        formset = ServersForm(request.POST)
        print(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "New server has been added successfully!")
        else:
            messages.error(request, formset.errors)
        form = ServersForm()
        return render(request, 'ovpn/servers.html', {"servers": servers, "form": form})
    else:
        return render(request, 'ovpn/servers.html', {"servers": servers, "form": form})


def server_delete(request):
    if request.method != 'POST':
        return HttpResponse("Page not found", status=404)
    else:
        service_uuid = request.POST.get('service_uuid')
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
    server = get_object_or_404(Servers, id=sid)

    if request.method == 'GET':
        context = {'form': ServersForm(instance=server), 'id': sid}
        return render(request, 'ovpn/server_update.html', context)

    elif request.method == 'POST':
        form = ServersForm(request.POST, instance=server)
        print("POST: " + str(request.POST))
        if form.is_valid():
            form.save()
            messages.success(request, 'The service has been updated successfully.')
            return redirect('ovpn:servers')
        else:
            messages.error(request, 'Please correct the following errors: ' + str(form.errors))
            context = {'form': ServersForm(instance=server), 'id': sid}
            return render(request, 'ovpn/server_update.html', context)


def users(request):
    return render(request, 'ovpn/users.html')


def show_settings(request):
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
    res = ''
    for key, value in request.session.items():
        res += '</br>'
        res += str(key)
        res += ':'
        res += str(value)
    return HttpResponse(res)