from django.shortcuts import render
from .models import User
from .forms import UserForm

# Create your views here.

def users(request):
    """ APP user list

    Args:
        request (django.http.request): django request object 

    Returns:
        tempalate: tempate auth/users.html
    """
    form = UserForm()  
    users = User.objects.all()
    context = {"users": users, "form": form}
    return render(request, 'auth/users.html', context)