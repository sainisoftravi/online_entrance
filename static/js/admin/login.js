function validateForm(){
    success = true;
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;

    emailValue = document.getElementsByName('email')[0].value.trim();
    passwordValue = document.getElementsByName('new_password1')[0].value.trim();

    emailError = document.querySelector('.email-error');
    passwordError = document.querySelector('.password-error');

    if(!email_regex.test(emailValue)){
        success = false;
        emailError.innerText = 'Invalid Email';
        emailError.classList.add('show-error');
    }

    else{
        emailError.classList.remove('show-error');
    }

    if(!passwordValue){
        success = false;
        passwordError.innerText = 'This field must not be empty';
        passwordError.classList.add('show-error');
    }

    else{
        passwordError.classList.remove('show-error');
    }

    return success == true;
}
