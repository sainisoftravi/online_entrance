feedBack = document.querySelector('.show-success-feedback-message');


setTimeout(function() {
    $(feedBack).fadeOut('fast');
}, 1500); // <-- time in milliseconds


function validateFeedBackForm(){
    success = true;
    name_regex = /^[A-Za-z\s]+$/;
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;

    name_error = document.querySelector('.name-error');
    email_error = document.querySelector('.email-error');
    message_error = document.querySelector('.message-error');

    contact_name = document.querySelector('#contact-name');
    contact_email = document.querySelector('#contact-email');
    contact_message = document.querySelector('#contact-message');

    contact_name_value = contact_name.value.trim();
    contact_email_value = contact_email.value.trim();
    contact_message_value = contact_message.value.trim();

    if(!contact_name_value || !(name_regex.test(contact_name_value))){
        success = false;
        name_error.classList.add('sho-error')
        name_error.innerText = 'Name must contain letter(s)';
    }

    else{
        name_error.classList.remove('sho-error')
    }

    if(!contact_email_value || !(email_regex.test(contact_email_value))){
        success = false;
        email_error.classList.add('sho-error')
        email_error.innerText = 'Invalid email';
    }

    else{
        email_error.classList.remove('sho-error')
    }

    if(!contact_message_value){
        success = false;
        message_error.classList.add('sho-error')
        message_error.innerText = 'Message must not be empty';
    }

    else{
        message_error.classList.remove('sho-error')
    }

    console.log(success);
    return success == true;
}
