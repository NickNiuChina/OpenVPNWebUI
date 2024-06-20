// not working currently
$(document).ready(function() {

    // if set these to local variable, will cause modal submit too many times
    var cn;
    var storename;

    // Result message
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
    const appendAlert = (message, type) => {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible fade show " role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="close" data-dismiss="alert" aria-label="Close">',
            '<span aria-hidden="true">&times;</span>',
            '</button>',
            '</div>'
        ].join('\n');

        alertPlaceholder.append(wrapper);
    };

    function formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        return [year, month, day].join('-');
    };

    function formatTime(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + d.getHours(),
            min = '' + d.getMinutes(),
            sec = '' + d.getSeconds();
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        if (hour.length < 2) {
            hour = '0' + hour;
        }
        if (min.length < 2) min = '0' + min;
        if (sec.length < 2) sec = '0' + sec;
        return [year, month, day].join('-') + "_" + [hour, min, sec].join(':');
    };

    /*
       nav highlight when a.href == location.pathname
   */

    $(".nav-item").find("li").each(function() {
        var a = $(this).find("a:first")[0];
        // console.log(a);
        if ($(a).attr("href") === location.pathname) {
            $(a).addClass("active");
            // console.log("==========================");
        } else {
            $(a).removeClass("active");
            // console.log("nnnnnnnnnnnnnnnnnnnnnnnnnnnnn");
        }
    });

    /*
        nav highlight when a.href == location.pathname
    */
    $(".nav-sidebar").find("li").each(function() {
        var a = $(this).find("a:first")[0];
        if ($(a).attr("href") === location.pathname) {
            $(a).addClass("active");
        } else {
            $(a).removeClass("active");
        }
    });


    /* **********************************************
        OpenVPN serivces page
    ********************************************** */
    // Post to stop an OpenVPN service
    $('tbody').on('click', '.stop_ovpn_service', function() {
        // alert("debug");
        $tr = $(this).closest('tr');
        var data = $tr.children("th").map(function() {
            return $(this).text();
        }).get();

        var current_ob = $(this).closest('tr').find(".server_running_status");

        var s_uuid = data[0];
        // alert(sid);
        $.post("", { 'csrfmiddlewaretoken': window.csrftoken, 'action': "stop", "s_uuid": s_uuid }, function(result) {
            // alert("debug in jQuery post");
            // window.location.reload();
            // $tr.find(".server_running_status").addClass("text-green").removeClass("text-red");
            if (result['result'] == 'success') {
                current_ob.removeClass("text-green").addClass("text-red");
            }
            appendAlert(result['message'], result['result']);
        });
    });

    // Post to stop an OpenVPN service
    $('tbody').on('click', '.start_ovpn_service', function() {
        // alert("debug");
        $tr = $(this).closest('tr');
        var data = $tr.children("th").map(function() {
            return $(this).text();
        }).get();

        var current_ob = $(this).closest('tr').find(".server_running_status");

        var s_uuid = data[0];
        // alert(sid);
        $.post("", { 'csrfmiddlewaretoken': window.csrftoken, 'action': "start", "s_uuid": s_uuid }, function(result) {
            // alert("debug in jQuery post");
            // window.location.reload();
            // $tr.find(".server_running_status").addClass("text-red").removeClass("text-green");
            if (result['result'] == 'success') {
                current_ob.removeClass("text-red").addClass("text-green");
            }
            appendAlert(result['message'], result['result']);
        });
    });

    /* **********************************************
        OpenVPN serivce pages, like clients list or certs .......
    ********************************************** */
    // Plain cert page: delete a plain cert
    $('tbody').on('click', '.delete_plain_cert', function() {
        // alert("debug");
        $('#delete_plain_cert_modal').modal('show');
        $tr = $(this).closest('tr');
        var data = $tr.children("th").map(function() {
            return $(this).text();
        }).get();

        $('#delete_plain_cert').val(data[0]);
    });

    // Plain cert page: download a plain cert
    // https://stackoverflow.com/questions/69017507/download-file-via-ajax-results-in-corrupted-file
    $('tbody').on('click', '.download_plain_cert', function() {
        // alert("debug");
        $tr = $(this).closest('tr');
        var data = $tr.children("th").map(function() {
            return $(this).text();
        }).get();
        // alert(data[0]);
        var plain_cert_filename = data[0];
        $.ajax({
            type: "post",
            url: "",
            data: { 'csrfmiddlewaretoken': window.csrftoken, 'action': "download_plain_cert", "download_plain_cert": plain_cert_filename },
            cache: false,
            xhr: function() {
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 2) {
                        if (xhr.status == 200) {
                            xhr.responseType = "blob";
                        } else {
                            xhr.responseType = "text";
                        }
                    }
                };
                return xhr;
            },
            success: function(data) {
                //Convert the Byte Data to BLOB object.
                var blob = new Blob([data], { type: "application/octetstream" });

                //Check the Browser type and download the File.
                var isIE = false || !!document.documentMode;
                if (isIE) {
                    window.navigator.msSaveBlob(blob, plain_cert_filename);
                } else {
                    var url = window.URL || window.webkitURL;
                    link = url.createObjectURL(blob);
                    var a = $("<a />");
                    a.attr("download", plain_cert_filename);
                    a.attr("href", link);
                    $("body").append(a);
                    a[0].click();
                    $("body").remove(a);
                }
            }
        });
    });
});

$(document).ready(function() {
    function createEditor(name, size, theme, mode, readonly) {
        // find the textarea
        var textarea = document.querySelector("form textarea[name=" + name + "]");

        // create ace editor
        var editor = ace.edit()
        editor.container.style.height = size

        editor.setTheme("ace/theme/" + theme); //"clouds_midnight"
        //editor.setTheme("ace/theme/twilight");
        //editor.setTheme("ace/theme/iplastic");

        editor.session.setMode("ace/mode/" + mode);

        editor.setReadOnly(readonly);
        editor.setShowPrintMargin(false);
        editor.session.setUseWrapMode(true);
        editor.session.setValue(textarea.value)
            // replace textarea with ace
        textarea.parentNode.insertBefore(editor.container, textarea)
        textarea.style.display = "none"
            // find the parent form and add submit event listener
        var form = textarea
        while (form && form.localName != "form") form = form.parentNode
        form.addEventListener("submit", function() {
            // update value of textarea to match value in ace
            textarea.value = editor.getValue()
        }, true)
    };
});