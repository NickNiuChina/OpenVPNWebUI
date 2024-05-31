from django.shortcuts import render
from .models import User

# Create your views here.

def users(request):
    """ APP user list

    Args:
        request (django.http.request): django request object 

    Returns:
        tempalate: tempate auth/users.html
    """
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'auth/users.html', context)