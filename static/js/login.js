email_box = document.querySelector('#email');
form_right = document.querySelector('.form-right');
password_box = document.querySelector('#password');
email_error = document.querySelector('.email-error');
submit_button = document.querySelector('.submit-btn');
password_error = document.querySelector('.password-error');

function validateForm(){
    success = true;
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;

    password = password_box.value;
    email_value = email_box.value;

    if(!email_value || email_value.indexOf(' ') != -1 || (email_value.indexOf('@') != -1 && email_regex.test(email_value) == false)){
        success = false;
        email_error.innerHTML = 'Invalid Email';
        email_error.classList.add('show-error');
    }

    else{
        email_error.classList.remove('show-error');
    }

    if(!password){
        success = false;
        password_error.innerHTML = "Invalid Password"
        password_error.classList.add('show-error');
    }

    else{
        password_error.classList.remove('show-error');
    }

    return success == true;
}
