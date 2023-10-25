function changePassword(){
    success = true;

    oldPasswordError = document.querySelector('.old_password_error');
    newPasswordError = document.querySelector('.new_password1_error');
    newPasswordAgainError = document.querySelector('.new_password2_error');
    oldPassword = document.getElementsByName('old_password')[0].value.trim();
    newPassword = document.getElementsByName('new_password1')[0].value.trim();
    newPasswordAgain = document.getElementsByName('new_password2')[0].value.trim();

    if(!oldPassword){
        success = false;
        oldPasswordError.classList.add('show-error');
    }

    else{
        oldPasswordError.classList.remove('show-error');
    }

    if(!newPassword){
        success = false;
        newPasswordError.classList.add('show-error');
    }

    else{
        newPasswordError.classList.remove('show-error');
    }


    if(!newPasswordAgain){
        success = false;
        newPasswordAgainError.classList.add('show-error');
    }

    else if(newPassword != newPasswordAgain){
        success = false;
        newPasswordAgainError.innerText = 'New Passwords did not match';
        newPasswordAgainError.classList.add('show-error');
    }

    else if(oldPassword == newPassword){
        success = false;
        newPasswordAgainError.innerText = 'Old and New Password must not be same';
        newPasswordAgainError.classList.add('show-error');
    }

    else{
        newPasswordError.classList.remove('show-error');
    }

    return success == true;
}


window.onload = () => {
    oldPassword = document.getElementsByName('old_password')[0];
    newPassword = document.getElementsByName('new_password1')[0];
    newPasswordAgain = document.getElementsByName('new_password2')[0];

    old_password_eye = document.querySelector('.old_password_eye');
    new_password_eye = document.querySelector('.new_password1_eye');
    new_confirm_password_eye = document.querySelector('.new_password2_eye');

    all_inputs = [oldPassword, newPassword, newPasswordAgain];
    all_eyes = [old_password_eye, new_password_eye, new_confirm_password_eye]

    all_inputs.forEach((input_box, index) => {
        input_box.addEventListener('input', (event) => {
            input_value = input_box.value.length;

            if(input_value == 0){
                all_eyes[index].classList.add('hide-eye');
            }

            else{
                all_eyes[index].classList.remove('hide-eye');
            }
        });
    });

    all_eyes.forEach((eye, index) => {
        eye.addEventListener('click', (event) => {
            eye.classList.toggle('bxs-show');
            input_box = all_inputs[index];

            if(input_box.type == 'password'){
                input_box.type = 'text';
            }

            else{
                input_box.type = 'password';
            }
        });
    });
}
