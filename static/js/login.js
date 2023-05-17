form_right = document.querySelector('.form-right');
password_box = document.querySelector('#Password');
user_email_box = document.querySelector('#Username');
submit_button = document.querySelector('.submit-btn');
hide_password = document.querySelector('.hide-password');
show_password = document.querySelector('.show-password');
password_error = document.querySelector('.password-error');
user_email_error = document.querySelector('.username-error');
invalid_username_email_password = document.querySelector('.invalid-username-password');

hide_password.classList.add('show-hide-password');
show_password.classList.add('show-hide-password');

if(submit_button.value == 'Sign Up'){
    form_right.style = 'none;';
}

else{
    form_right.style = 'justify-content: center;';
}

function validateForm(){
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;
    password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    password = password_box.value;
    user_email_value = user_email_box.value;

    if((user_email_value.indexOf('@') != -1 && email_regex.test(user_email_value) == false) || !user_email_value){
        user_email_error.innerHTML = 'Invalid Username/Email';
        user_email_error.style.display = 'block';
    }

    else if(user_email_value.indexOf(' ') != -1){
        user_email_error.innerHTML = 'Username/Email must not contain space(s)';
        user_email_error.style.display = 'block';
    }
    else{
        user_email_error.style.display = 'none';
    }

    if(password_regex.test(password) == false){
        password_error.innerHTML = "Password must be a combination of letters, numbers, and special characters, with a minimum length of 8 characters"
        password_error.style.display = 'block';
    }

    else{
        password_error.style.display = 'none';
    }
}

hide_password.addEventListener('click', function(){
    password_box.type = 'text';
    hide_password.classList.add('show-hide-password');
    show_password.classList.remove('show-hide-password');
});


show_password.addEventListener('click', function(){
    password_box.type = 'password';
    show_password.classList.add('show-hide-password');
    hide_password.classList.remove('show-hide-password');
});

password_box.addEventListener('keyup', (event) => {
    values = password_box.value

    if(values.length >= 1){
        if(hide_password.classList.contains('show-hide-password')){
            hide_password.classList.remove('show-hide-password');
        }
    }

    else if(values.length == 0){
        hide_password.classList.add('show-hide-password');
        show_password.classList.add('show-hide-password');
    }
});
