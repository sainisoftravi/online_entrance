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


window.addEventListener('load', function() {
    reported_textarea = document.getElementsByClassName('reported');

    if(reported_textarea){
        reported_textarea = reported_textarea[0];
        console.log(reported_textarea);

        reported_textarea.addEventListener('mousedown', (e) => {
            e.preventDefault();
        });
    }
});
