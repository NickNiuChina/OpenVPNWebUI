1. Install  apache2
2. copy openvpn_webui.conf to /etc/apache2/site-available, create link from conf-enabled to this file,
    and change the config as your environment.
3. In /opt/ote clone this code and create python virtualenv
    ls -al
    drwxr-xr-x 10 root root 4096 Jun 24 13:43 OpenVPNWebUI
    drwxr-xr-x  5 root root 4096 Jun 24 13:19 ote_venv
4. in /var/www apache dir, create link:
    ln -s /opt/ote/ ote

5. log dir chown
    chown www-data:www-data /var/log/apach2/ -R

6. Enable some modules
    a2enmod rewrite
    a2enmod proxy
    a2enmod ssl
    