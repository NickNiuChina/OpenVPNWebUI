1. jQuery Knob 自动刷新

```commandline
<input type="text" class="dial" value="75">


// 初始化 Knob
$('.dial').knob({
    // 这里可以配置 Knob 的其他选项，如 min, max, step 等
});
 
// 自动刷新 Knob 的值
function updateKnob() {
    // 这里假设我们想要每秒更新一次值，范围在 0 到 100 之间
    var newValue = Math.floor(Math.random() * 100); // 随机生成一个新值
    $('.dial').val(newValue).trigger('change'); // 设置新的值并触发 change 事件来更新 Knob
}
 
// 每秒调用一次 updateKnob 函数来更新 Knob 的值
setInterval(updateKnob, 1000); // 每秒更新一次
```



2.  password encryption

   ```
   from django.contrib.auth.hashers import make_password
   from django.contrib.auth.hashers import check_password
   ```

3.  OpenVPN client
    ```commandline
    cat vpn-client-download.sh
    #!/bin/sh
    DESTPATH="$1"
    VPN_FOLDER=/opt/vpnclient
    #if uuid was not generated yet, generate all files
    if [[ ! -f $VPN_FOLDER/device_uuid ]]
    then
            /home/webui/pvshell-web/scripts/vpn-client-reset.sh 0
    #if cert, password or key are missing, re-generate them
    elif [[ ! -f $VPN_FOLDER/device_password ]] || [[ ! -f $VPN_FOLDER/device_cert ]] || [[ ! -f $VPN_FOLDER/device_key ]]
    then
            /home/webui/pvshell-web/scripts/vpn-client-reset.sh 1
    fi
    
    #if cert is about to expire (less than 30 days), re-generate it
    /home/webui/pvshell-web/scripts/vpn-client-check-cert.sh > /dev/null 2>&1
    
    cat $VPN_FOLDER/device_uuid $VPN_FOLDER/device_password $VPN_FOLDER/device_cert > $VPN_FOLDER/$(<$VPN_FOLDER/device_uuid).req
    
    #PATH=??? used to generate a blob
    if [[ $DESTPATH = "???" ]];then
            cat $VPN_FOLDER/*.req
            rm $VPN_FOLDER/*.req > /dev/null 2>&1
    else
            FILENAME=`basename $(ls $VPN_FOLDER/*.req)`
            mv $VPN_FOLDER/*.req $DESTPATH
            echo -n $FILENAME
    fi
    sync
    exit 0
    
    ### 
    
    cat /home/webui/pvshell-web/scripts/vpn-client-reset.sh
    #!/bin/sh
    DEPTH=${1:-"2"}
    VPN_FOLDER=/opt/vpnclient
    CONF_FOLDER=/etc/openvpn
    #DEPTH 0: complete clean up of /opt/vpnclient: remove device_uuid too. Useful to get to a starting condition.
    #DEPTH 1: re-generate certificate, key and password. Useful when certificate is about to expire.
    #DEPTH 2: delete imported .conf files (udp and tcp) and returns to server configuration. Useful when there are overwrite issues (default).
    
    cd "$VPN_FOLDER"
    if [ "$DEPTH" -eq 0 ]; then
            rm -rf device_uuid
    
            #NEW_UUID
            [[ -r device_uuid ]] || uuidgen --time > device_uuid
    fi
    if [ "$DEPTH" -le 1 ]; then
            rm -rf device_password
            rm -rf device_cert
            rm -rf device_key
    
            #NEW_PASSWORD
            [[ -r device_password ]] || (</dev/urandom tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' | head -c 20 ; echo) > device_password
            #NEW_CERT
            openssl req -x509 -newkey rsa:4096 -nodes -keyout device_key -out device_cert -days 366 -subj "/CN=$(<device_uuid)"
    fi
    if [ "$DEPTH" -eq 2 ]; then
            rm -rf $CONF_FOLDER/client_conf/*
            cp $CONF_FOLDER/server_conf/openvpn.conf $CONF_FOLDER/openvpn.conf
            echo "" > /var/log/openvpn.log
            sed -i 's/client/server/g' $CONF_FOLDER/config.json
    fi
    
    exit 0
    
    
    ###
    
    cat /home/webui/pvshell-web/scripts/vpn-client-check-cert.sh
    #!/bin/sh
    VPN_FOLDER=/opt/vpnclient
    
    cd "$VPN_FOLDER"
    ((CA_MIN_VALIDITY_SECONDS = 30 * 86400))
    
    if [[ -f $VPN_FOLDER/device_cert ]];then
            openssl x509 -checkend $CA_MIN_VALIDITY_SECONDS -noout -in device_cert
            if [[ $? -ne 0 ]]; then
                    /home/webui/pvshell-web/scripts/vpn-client-reset.sh 1
            fi
    fi
    exit 0

4.  Initial Super User
```
from users.models import UserGroup
User.initial()
```

5. redirect to next url
```https://stackoverflow.com/questions/3209906/django-return-redirect-with-parameters
redirect_url = reverse('my_function', args=(backend,))
parameters = urlencode(form.cleaned_data)
return redirect(f'{redirect_url}?{parameters}')
```

0. datas
```
python .\manage.py shell
from ovpn.models import Servers, ClientList
s = Servers.objects.filter(id='178dcc60c7a947c29ca45dc55cef0a4b').first()
c = ClientList(server=s, cn="nick-test", ip="1.1.1.1")
c = ClientList(server=s, cn="nick-test2", ip="2.2.2.2")
c = ClientList(server=s, cn="nick-test3", ip="3.3.3.3")
c.save()
```

o.

datatables pagelength
```
$(document).ready(function() {
    $('#example').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "your-server-side-script.php", // 服务器端脚本URL
            "type": "POST"
        },
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]], // 这里可以设置一个默认的分页长度选项
        "pageLength": -1, // 默认显示所有数据，直到用户手动改变
        "initComplete": function(settings, json) {
            var defaultPageLength = yourDatabaseFetchedValue; // 从数据库获取的默认分页长度值
            this.api().columns().every(function() {
                var column = this;
                if (column.index() == 0) { // 假设我们是根据第一列来设置分页长度
                    column.data().unique().sort().each(function(d, j) {
                        var pageLength = defaultPageLength; // 使用从数据库获取的值
                        var option = '<option value="' + pageLength + '">' + pageLength + '</option>';
                        $('#example_length').append(option); // 添加到选择框中
                    });
                }
            });
        }
    });
});
```