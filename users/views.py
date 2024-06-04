from django.shortcuts import render
from .models import User
from .forms import UserForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
import uuid


def users(request):
    """ APP user list

    Args:
        request (django.http.request): django request object 

    Returns:
        tempalate: tempate auth/users.html
    """
    form = UserForm()
    users_list = User.objects.all()
    context = {"users": users_list, "form": form}
    if request.method == "POST":
        formset = UserForm(request.POST)
        if formset.is_valid():
            if formset.data['password'] == formset.data['confirm_password']:
                user = formset.save(commit=False)
                user.password = make_password(user.password)
                user.save()
                messages.success(request, "New server has been added successfully!")
            else:
                messages.error(request, "Password does match, please check!")
        else:
            messages.error(request, formset.errors)
        return redirect("users:users")
    else:
        return render(request, 'auth/users.html', context)


def user_delete(request):
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
        user_uuid = request.POST.get('user_uuid', '')
        if user_uuid and user_uuid.strip():
            try:
                sid = uuid.UUID(user_uuid)
            except:
                sid = ''
            if sid:
                user = User.objects.get(id=sid)
                if not user:
                    messages.error(request, "This uuid isn't in records!")
                else:
                    if user.username == 'super':
                        messages.error(request, "This use can't be deleted!")
                    else:
                        user.delete()
                        messages.success(request, "User has been deleted successfully!")
                return redirect("users:users")
            else:
                messages.error(request, "Please provide a valid uuid!")
                return redirect("users:users")
        else:
            messages.error(request, "UUID is required for this request")
            return redirect("users:users")


def user_update(request, sid=None):
    """ OpenVPN server update

    Args:
        request (_type_): _description_
        sid (_type_): _description_

    Returns:
        _type_: _description_
    """
    user = get_object_or_404(User, id=sid)
    if request.method == 'GET':
        form = UserForm(instance=user)
        context = {'form': form, 'id': sid}
        return render(request, 'auth/user_update.html', context)
    elif request.method == 'POST':
        formset = UserForm(request.POST, instance=user)
        if formset.is_valid():
            if formset.data['password'] == formset.data['confirm_password']:
                user = formset.save(commit=False)
                user.password = make_password(user.password)
                user.save()
                messages.success(request, "User has been updated successfully!")
            else:
                messages.error(request, "Password does match, please check!")
            return redirect('ovpn:servers')
        else:
            messages.error(request, 'Please correct the following errors: ' + str(formset.errors))
            context = {'form': UserForm(instance=user), 'id': sid}
            return redirect("users:user_update", sid=sid)
        