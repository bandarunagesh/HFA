var data=[];

function addBr(text){
    return text.replace(/\n/g, "<br />");

}
var Message;
Message = function (arg) {
    this.text = arg.text, this.message_side = arg.message_side;
    this.draw = function (_this) {
        return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(addBr(_this.text));
            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};


function showBotMessage(msg){
        msg1=msg.split("!")
        
        message = new Message({
             text: msg1[0],
             message_side: 'left'
        });
        
        if(msg1.length > 1){
            // window.alert(msg1.length)
            if(msg1.length == 2){
                
                document.getElementsByClassName('btn_txt4')[0].innerHTML = msg1[1];
                document.getElementsByClassName('btn4')[0].style.visibility = "visible";
                document.getElementsByClassName('btn1')[0].style.visibility = "hidden";
                document.getElementsByClassName('btn2')[0].style.visibility = "hidden";
                document.getElementsByClassName('btn3')[0].style.visibility = "hidden";
                document.getElementsByClassName('quick_resp_btns')[0].style.visibility="visible"
            }
            if(msg1.length == 3){
                document.getElementsByClassName('btn_txt4')[0].innerHTML = msg1[1];
                document.getElementsByClassName('btn_txt3')[0].innerHTML = msg1[2];
                document.getElementsByClassName('btn4')[0].style.visibility = "visible";
                document.getElementsByClassName('btn3')[0].style.visibility = "visible";
                document.getElementsByClassName('btn1')[0].style.visibility = "hidden";
                document.getElementsByClassName('btn2')[0].style.visibility = "hidden";
                document.getElementsByClassName('quick_resp_btns')[0].style.visibility="visible"
            }
            if(msg1.length == 4){
                document.getElementsByClassName('btn_txt4')[0].innerHTML = msg1[1];
                document.getElementsByClassName('btn_txt3')[0].innerHTML = msg1[2];
                document.getElementsByClassName('btn_txt2')[0].innerHTML = msg1[3];
                document.getElementsByClassName('btn4')[0].style.visibility = "visible";
                document.getElementsByClassName('btn3')[0].style.visibility = "visible";
                document.getElementsByClassName('btn2')[0].style.visibility = "visible";                
                document.getElementsByClassName('btn1')[0].style.visibility = "hidden";
                document.getElementsByClassName('quick_resp_btns')[0].style.visibility="visible"
            }
            if(msg1.length == 5){
                document.getElementsByClassName('btn_txt4')[0].innerHTML = msg1[1];
                document.getElementsByClassName('btn_txt3')[0].innerHTML = msg1[2];
                document.getElementsByClassName('btn_txt2')[0].innerHTML = msg1[3];
                document.getElementsByClassName('btn_txt1')[0].innerHTML = msg1[4];
                document.getElementsByClassName('btn4')[0].style.visibility = "visible";
                document.getElementsByClassName('btn3')[0].style.visibility = "visible";
                document.getElementsByClassName('btn2')[0].style.visibility = "visible";
                document.getElementsByClassName('btn1')[0].style.visibility = "visible";
                document.getElementsByClassName('quick_resp_btns')[0].style.visibility="visible"
            }
        }
        else{
            document.getElementsByClassName('btn1')[0].style.visibility = "hidden";
            document.getElementsByClassName('btn2')[0].style.visibility = "hidden";
            document.getElementsByClassName('btn3')[0].style.visibility = "hidden";
            document.getElementsByClassName('btn4')[0].style.visibility = "hidden";
            // document.getElementsByClassName('btn4')[0].style.visibility = "visible";
            // document.getElementsByClassName('btn3')[0].style.visibility = "visible";
            // document.getElementsByClassName('btn2')[0].style.visibility = "visible";
            // document.getElementsByClassName('btn1')[0].style.visibility = "visible";
        }
        message.draw();
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
}
function showUserMessage(msg){
        $messages = $('.messages');
        message = new Message({
            text: msg,
            message_side: 'right'
        });
        message.draw();
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        $('#msg_input').val('');
}
function sayToBot(text){
    document.getElementById("msg_input").placeholder = "Type your messages here ....."
    $.post("/chat",
            {
                //csrfmiddlewaretoken:csrf,
                text:text,
            },
            function(jsondata, status){
                if(jsondata["status"]=="success"){
                    response=jsondata["response"];

                    if(response){showBotMessage(response);}
                }
            });

}

getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };

$("#say").keypress(function(e) {
    if(e.which == 13) {
        $("#saybtn").click();
    }
});

$('.btn1').click(function (e) {
        
    msg = getMessageText();
    if(msg){
    showUserMessage(msg);
    sayToBot(msg);
$('.message_input').val('');}
});


$('.send_message').click(function (e) {
        
        msg = getMessageText();
        if(msg){
        showUserMessage(msg);
        sayToBot(msg);
    $('.message_input').val('');}
});

$('.message_input').keyup(function (e) {
    if (e.which === 13) {
        msg = getMessageText();
        if(msg){
        showUserMessage(msg);
        sayToBot(msg);
    $('.message_input').val('') ;}
    }
});
