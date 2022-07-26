var objDiv = document.getElementById("chat-log");

//scrolls to bottom of chat log when loading the page
window.onload=function () {
    var objDiv = document.getElementById("chat-log");
    objDiv.scrollTop = objDiv.scrollHeight;
}

const chatID = JSON.parse(document.getElementById('chat-id').textContent);

const chatSocket = new ReconnectingWebSocket(
    'ws://'
    + window.location.host
    + '/ws/directmessage/'
    + chatID
    + '/'
);

function supportsPlaintextEditables () {
    var div = document.createElement('div');
    div.setAttribute('contenteditable', 'PLAINTEXT-ONLY');

    return div.contentEditable === 'plaintext-only';
}

if (supportsPlaintextEditables() == 1 ){
    document.getElementById('chat-message-input').setAttribute('contenteditable', 'plaintext-only')
}else{
    document.getElementById('chat-message-input').setAttribute('contenteditable', 'True')
}

$('#image_form').on('submit', function (e) {
        e.preventDefault();

        $form = $(this)
        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: 'save_image_message/',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,

            success: function (data) {

                if (data["status"] == "valid") {
                    

                    //Send data to websocket!
                    chatSocket.send(JSON.stringify({
                        'command': 'image',
                        'message': data['message'],
                        'user_id': data['user'],
                        'image_url': data['image_url'],
                        'date_sent': data['date_sent'],
                        'message_id':data['message_id']
                    }));

                    resetForm();


                }
                if (data["status"] == "invalid") {
                    console.log('Failed to upload image')
                }
            },
            error: function () {
                console.log('Failed to upload image')
            }
        })

    })

function deleteMessage(message_id){

    if (window.confirm("Are you sure you want to delete this message?")){

        $.ajax({
            type: 'GET',
            url: 'delete_message/',
            data: {messageID: message_id},

            success: function (data) {

                // tell websocket that the message was deleted...
                chatSocket.send(JSON.stringify({
                    'command': 'delete',
                    'message_id': message_id
                }));

            },
            error: function () {
                console.log("Failed to delete message")
            }
        })
    }
}

//Called after user selects custom button to select hidden "choose file" button
function chooseFile(){
    document.querySelector('#id_image').click();
}

// Called after user submits form via ajax
function resetForm(){
    document.getElementById('image_form').reset()
    document.getElementById('attachment-icon').setAttribute('hidden', 'True')
}

// Show attachment is selected after user has chosen it
$('#id_image').on('change', function(){
    //TODO 
    document.getElementById('attachment-icon').removeAttribute("hidden")
})

//Variable Used for timing out who is typing...
let timeout;

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


document.querySelector('#chat-message-input').focus();

document.querySelector('#chat-message-input').onkeydown = function(e) {
   // User hits enter key and is not holding shift
   if (e.keyCode === 13 && event.shiftKey != 1) {

        //This prevents the div from expanding
        e.preventDefault()
    }
};

function removeWhoIsTyping(user_id){

    if (user_id === ''){
        document.getElementById('who-is-typing').innerHTML = ""

    }else{

        string_to_remove = user_id + ' is typing'
        document.getElementById('who-is-typing').innerHTML = document.getElementById('who-is-typing').innerHTML.replace(string_to_remove, '')
    }
};