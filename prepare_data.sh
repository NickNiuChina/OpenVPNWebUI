# standard user creation, NOT USED in this project
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# customization user create
echo "from users.models import User; User.initial()" | python manage.py shell
echo "from ovpn.models import SystemCommonConfig; SystemCommonConfig.initial()" | python manage.py shell