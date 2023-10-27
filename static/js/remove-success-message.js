$(document).ready(function(){
    if($('.success-message-div').html().trim().length == 0) {
        $('.success-message-div').css('display', 'none');
    }

    else{
        success_message_div = document.querySelector('.success-message-div')

        setTimeout(function() {
            $(success_message_div).fadeOut('fast');
        }, 1500);
    }
});
