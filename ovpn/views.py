from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servers
import platform
import datetime
from .forms import ServersForm
import uuid
import datetime


def index(request):
    system_info = {
        'system_type': platform.system(),
        'system_version': platform.version(),
        'system_time': datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
        }
    return render(request, 'ovpn/main.html')


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