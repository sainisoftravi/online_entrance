function changePassword(){
    success = true;

    oldPasswordError = document.querySelector('.old-password-error');
    newPasswordError = document.querySelector('.new-password-error');
    oldPassword = document.getElementsByName('old_password')[0].value.trim();
    newPassword = document.getElementsByName('new_password1')[0].value.trim();
    newPasswordAgain = document.getElementsByName('new_password2')[0].value.trim();
    newPasswordAgainError = document.querySelector('.new-password-again-error');

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
