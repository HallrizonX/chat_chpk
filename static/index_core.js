$(document).ready(function () {
    var ROOM_DIV = 'room_message_';
    window.userSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
    window.localDict = {};

    userSocket.onmessage = function (e) {
        console.log('USER SOCKET');
        console.log('USER SOCKET');
        var data = JSON.parse(e.data);
        for (room_id in data) {
            var count = data[room_id];
            var room = $("#" + ROOM_DIV + room_id);
            if (count > 0) {

                if (window.localDict[room_id] == undefined || window.localDict[room_id] < count) {
                    window.M.toast({html: 'Чат: ' + room.find('.room-title').text().trim()});
                    window.localDict[room_id] = count;
                }

            }
            $(room).find('.badge').text(count);
        }
    };


    $(".room").on('click', function (e) {
        e.preventDefault();
        try {
            window.chatSocket.close();
        } catch (e) {
        }
        $.ajax({
            url: $(this).attr('href'),
            beforeSend: function () {
                $(".chat-field").html('').append('<div class="progress">\n' +
                    '      <div class="indeterminate"></div>\n' +
                    '  </div>')
            }
        }).done(function (data) {
            $(".chat-field").html('');
            $(".chat-field").append(data);
        });
    })


});