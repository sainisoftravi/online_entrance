cross_close = document.querySelector('.cross-close')
changeProfileForm = document.getElementById('changeProfileForm');
changeProfileButton = document.getElementById('changeProfileButton');
successMessageDiv = document.querySelector('.success-message-div');


changeProfileButton.addEventListener('change', () => {
    if(changeProfileButton.files.length != 0){
        changeProfileForm.submit();
    }
});


cross_close.addEventListener('click', () => {
    successMessageDiv.classList.add('remove');
});


function changePassword(){
    success = true;
    oldPassword = document.querySelector('#OldPassword').value;
    newPassword = document.querySelector('#NewPassword').value;
    newPasswordAgain = document.querySelector('#NewPasswordAgain').value;

    oldPasswordError = document.querySelector('.old-password-error');
    newPasswordError = document.querySelector('.new-password-error');
    newPasswordAgainError = document.querySelector('.new-password-again-error');

    if(!oldPassword){
        oldPasswordError.innerText = 'This field must not be empty';
        newPasswordError.classList.remove('remove-password-error');
        oldPasswordError.classList.add('show-password-error');

        success = false;
    }

    else{
        oldPasswordError.classList.add('remove-password-error');
        success = true;
    }

    if(!newPassword){
        newPasswordError.innerText = 'This field must not be empty';
        newPasswordError.classList.remove('remove-password-error');
        newPasswordError.classList.add('show-password-error');
        success = false;
    }

    else{
        newPasswordError.classList.remove('show-password-error');
        newPasswordError.classList.add('remove-password-error');
        success = true;
    }


    if(!newPasswordAgain){
        newPasswordAgainError.innerText = 'This field must not be empty';
        newPasswordError.classList.remove('remove-password-error');
        newPasswordAgainError.classList.add('show-password-error');
        success = false;
    }

    else{
        newPasswordError.classList.remove('show-password-error');
        newPasswordAgainError.classList.add('remove-password-error');
        success = true;
    }

    if(newPassword && newPasswordAgain){
        console.log(newPassword != newPasswordAgain);

        if(newPassword != newPasswordAgain){
            newPasswordAgainError.innerText = 'New Passwords did not match';
            newPasswordAgainError.classList.remove('remove-password-error');
            newPasswordAgainError.classList.add('show-password-error');
            success = false;
        }

        else{
            newPasswordError.classList.remove('show-password-error');
            newPasswordAgainError.classList.add('remove-password-error');
            success = true;
        }
    }

    return success == true;
}
