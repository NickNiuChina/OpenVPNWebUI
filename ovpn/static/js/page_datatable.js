$(document).ready(function() {
    // client status table
    var tunTBclientStatus = $("#" + current_tableid).DataTable({
        //"dom": 'Blfrtip',
        "dom": '<"row"<"col"B><"col"f>>rt<"row"<"col"i><"col"p>>',
        "responsive": true,
        "lengthChange": true,
        "autoWidth": false,
        "pageLength": table_pagesize ? table_pagesize : 50,
        // "responsive": true, "lengthChange": true, "autoWidth": true,
        //"buttons": ["excel", "colvis"],
        "buttons": [{
                extend: 'excel',
                text: 'Excel',
                exportOptions: {
                    modifier: {
                        page: 'all',
                        selected: null,
                        search: 'none',
                    },
                    columns: [0, 1, 2, 3, 4, 5, 6]
                },
            },
            // { extend: 'excel', text: '<i class="fas fa-file-excel" aria-hidden="true"> Excel </i>' },
            "colvis",
            "pageLength"
        ],

        "lengthMenu": [50, 100, 200, "500", { label: 'All', value: -1 }],
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "paging": true,
        //"search": {return: true },
        "ordering": true,
        "order": [5, "desc"],
        "ajax": {
            'url': "",
            'type': 'POST',
            'data': {
                'csrfmiddlewaretoken': window.csrftoken,
                'action': "list"
            },
            'dataType': 'json',
        },
        "columnDefs": [{
                "targets": 0,
                "data": null,
                // "className": "edit_site_name",
                // createdCell: function(cell) {
                //     cell.setAttribute('data-toggle', 'modal');
                //     $(cell).css('color', 'blue');
                // },
                "render": function(data, type, row) {
                    // return data["site_name"];
                    var site_name = data["site_name"] ? data["site_name"] : "Unnamed";
                    // data-target='#updateClientSiteName'
                    var html = "<a href='javascript:void(0);'  class='edit_site_name' data-toggle='modal' >" + site_name + "</a>"
                    return html;
                }
            },
            {
                "targets": 1,
                "data": null,
                "render": function(data, type, row) {
                    return data["cn"];
                }
            },
            {
                "targets": 2,
                "data": null,
                "render": function(data, type, row) {
                    return data["ip"];
                }
            },
            {
                "targets": 3,
                "data": null,
                "render": function(data, type, row) {
                    var rdate = new Date(data["toggle_time"])
                        // console.log(formatDate(rdate));
                        // return formatTime(rdate);
                    return data["toggle_time"];
                }
            },
            {
                "targets": 4,
                "data": null,
                "render": function(data, type, row) {
                    var rdate = new Date(data["expire_date"])
                        // console.log(formatDate(rdate));
                        // return formatDate(rdate);
                    return data["expire_date"];
                }
            },
            {
                "targets": 5,
                "data": null,
                "render": function(data, type, row) {
                    // console.log(data[5]);
                    var html = data["status"] ? "<i class='fa fa-circle text-green'></i>" : "<i class='fa fa-circle text-red'></i>";
                    return html;
                }
            },
            {
                "targets": 6,
                "orderable": false,
                "data": null,
                "render": function(data, type, row) {
                    // console.log(data[5]);
                    if (data["status"]) {
                        var reg = RegExp(/boss/);
                        if (data["cn"].length == 41 || reg.test(data["cn"])) {
                            var html = "<a href='javascript:void(0);' class='conn4ect443 btn btn-default btn-xs'><i class='far fa-arrow-alt-circle-right'></i> Mgmt</a>"
                            html += "<a href='javascript:void(0);' class='sshConnect btn btn-default btn-xs'><i class='fa fa-terminal'></i> SSH</a>"
                            return html;
                        } else {
                            var html = 'NotApplied';
                            return html;
                        }
                    } else {
                        var html = 'Unreachable';
                        return html;
                    }
                }
            },
            {
                "targets": 7,
                "orderable": false,
                "data": null,
                "render": function(data, type, row) {
                    if (data["status"]) {
                        var reg = RegExp(/boss/);
                        if (data["cn"].length == 41 || reg.test(data["cn"])) {
                            var html = "<a href='javascript:void(0);' class='checkProxyConfig btn btn-default btn-xs'><i class='fa fa-file'></i> proxy</a>"
                            return html;
                        } else {
                            var html = 'NotApplied';
                            return html;
                        }
                    } else {
                        var html = 'Unreachable';
                        return html;
                    }
                }
            },
        ],
        // hide the ProxyConfig check if it is not "super" or "admin"
        "initComplete": function(settings, json) {
            if (settings.jqXHR.responseJSON.privs_group != 'SUPER' && settings.jqXHR.responseJSON.privs_group != 'ADMIN') {
                // alert(settings.jqXHR.responseJSON.privs);
                // alert(json.privs_group);
                tunTBclientStatus.columns([7]).visible(false);
            }
            // alert(table_pagesize);
            // delete the default page size from user settings
            delete window.table_pagesize;
        },

    });

    // This works only if the datatables drawed by django not by datatables ajax
    // $('.edit_site_name').on('click', function(e) {
    //     e.preventDefault();
    //     $('#updateClientSiteName').modal('show');
    //     $tr = $(this).closest('tr');
    //     var data = $tr.children("td").map(function() {
    //         return $(this).text();
    //     }).get();

    //     console.log("xxxxxxxxxxx");
    //     $('#client_uuid').val(data[0]);
    //     $('#client_old_name').val(data[1]);
    // });

    $('tbody').on('click', '.edit_site_name', function() {
        $('#updateClientSiteName').modal('show');
        $tr = $(this).closest('tr');
        var data = $tr.children("td").map(function() {
            return $(this).text();
        }).get();

        $('#client_cn').val(data[1]);
        $('#client_old_name').val(data[0]);
    });

    // refresh every 30s
    setInterval(function() {
        tunTBclientStatus.ajax.reload();
    }, 30000);

});