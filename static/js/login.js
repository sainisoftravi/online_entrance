email_box = document.querySelector('#email');
form_right = document.querySelector('.form-right');
password_box = document.querySelector('#password');
email_error = document.querySelector('.email-error');
submit_button = document.querySelector('.submit-btn');
password_error = document.querySelector('.password-error');
email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;


function validateForm(){
    success = true;

    password = password_box.value;
    email_value = email_box.value;

    if(!email_regex.test(email_value)){
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
