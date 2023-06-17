email_box = document.querySelector('#email');
form_right = document.querySelector('.form-right');
password_box = document.querySelector('#password');
email_error = document.querySelector('.email-error');
submit_button = document.querySelector('.submit-btn');
password_eye = document.querySelector('.password-eye');
password_error = document.querySelector('.password-error');

password_eye.classList.add('show-hide-password');

if(submit_button.value == 'Sign Up'){
    form_right.style = 'none;';
}

else{
    form_right.style = 'justify-content: center;';
}

function validateForm(){
    success = true;
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;

    password = password_box.value;
    email_value = email_box.value;

    if(!email_value || email_value.indexOf(' ') != -1 || (email_value.indexOf('@') != -1 && email_regex.test(email_value) == false)){
        email_error.innerHTML = 'Invalid Email';
        email_error.style.display = 'block';
        success = false;
    }

    else{
        email_error.style.display = 'none';
    }

    if(!password){
        password_error.innerHTML = "Invalid Password"
        password_error.style.display = 'block';
        success = false;
    }

    else{
        password_error.style.display = 'none';
    }

    return success == true;
}

password_eye.addEventListener('click', (event) => {
    if(password_box.type == 'text'){
        password_box.type = 'password';
        password_eye.classList.add('bxs-hide');
        password_eye.classList.remove('bxs-show');
    }

    else{
        password_box.type = 'text';
        password_eye.classList.add('bxs-show');
        password_eye.classList.remove('bxs-hide');
    }
});


password_box.addEventListener('keydown', (event) => {
    values = password_box.value

    if(values.length >= 1){
        if(password_eye.classList.contains('show-hide-password')){
            password_eye.classList.remove('show-hide-password');
        }
    }

    else if(values.length == 0){
        password_eye.classList.add('show-hide-password');
    }
});
