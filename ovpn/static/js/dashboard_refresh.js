$(document).ready(function() {
    function ds_refresh() {
        /**
        {"system_info":
            {
                "system_type":"Windows",
                "system_version":"10",
                "system_time":"2024-06-02_20:49:03",
                "cpu_cores":12,
                "system_uptime":"3 days,2:32:57",
                "load_avg":[0,0,0],
                "memory_total":32490.8,
                "memory_used":15299.6,
                "memory_percent":47.1,
                "swap_total":4864,
                "swap_used":1,
                "swap_percent":0,
                "openvpn_version":"NA",
                "system_information":"Windows-10-10.0.22631-SP0"
            }
        }
        **/
        $.post("", { 'action': "db_refresh", 'csrfmiddlewaretoken': window.csrftoken }, function(result) {
            // console.log("Return from server: " + JSON.stringify(result));
            system_info = result.system_info;
            $("#db_system_type").text(system_info.system_type);
            $("#db_system_version").text(system_info.system_version);
            $("#db_cpu_cores").text(system_info.cpu_cores);
            $("#db_system_uptime").text(system_info.system_uptime);
            $("#db_system_time").text(system_info.system_time);
            $("#db_db_load_avg0").text(system_info.load_avg[0]);
            $("#db_db_load_avg1").text(system_info.load_avg[1]);
            $("#db_db_load_avg2").text(system_info.load_avg[2]);
            $("#db_memory").html("Memory <b>" + system_info.memory_used + "</b>/" + system_info.memory_total + " MB - " + system_info.memory_percent + " %");
            $("#db_swap").html("Swap <b>" + system_info.swap_used + "</b>/" + system_info.swap_total + " MB - " + system_info.swap_percent + " %");
            $("#db_openvpn_version").text(system_info.openvpn_version);
            $("#db_system_information").text(system_info.system_information);

            var memory_percent = parseFloat(system_info.memory_percent).toFixed(1);
            $('#memory_progressBar').css('width', memory_percent.toString() + '%');
            $('#momery_progressBar').html(memory_percent.toString() + '%');

            var swap_percent = parseFloat(system_info.swap_percent).toFixed(1);
            $('#swap_progressBar').css('width', swap_percent.toString() + '%');
            $('#swap_progressBar').html(swap_percent.toString() + '%');
        });
    };

    setInterval(ds_refresh, 10000);

});