backend_message = document.querySelector('.backend-message')

setTimeout(function() {
    $(backend_message).fadeOut('fast');
}, 1500);


function validateForm(){
    success = true;

    message = document.querySelector('#message').value.trim();
    error_message = document.querySelector('.error-message');

    if(!message){
        success = false;

        error_message.innerText = 'Issue must not be empty'
        error_message.classList.add('sho-error');
    }

    else if(message.split(' ').length < 50){
        success = false;
        error_message.innerText = 'Issue must have at least 50 words';
        error_message.classList.add('sho-error');
    }

    else{
        error_message.classList.remove('sho-error');
    }

    return success == true;
}
