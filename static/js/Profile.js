changeProfileForm = document.getElementById('changeProfileForm');
successMessageDiv = document.querySelector('.success-message-div');
changeProfileButton = document.getElementById('changeProfileButton');

setTimeout(function() {
    $(successMessageDiv).fadeOut('fast');
}, 1500); // <-- time in milliseconds

changeProfileButton.addEventListener('change', () => {
    if(changeProfileButton.files.length != 0){
        changeProfileForm.submit();
    }
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
        success = false;
        oldPasswordError.classList.add('show-error');
    }

    else{
        success = true;
        oldPasswordError.classList.remove('show-error');
    }

    if(!newPassword){
        success = false;
        newPasswordError.classList.add('show-error');
    }

    else{
        success = true;
        newPasswordError.classList.remove('show-error');
    }


    if(!newPasswordAgain){
        success = false;
        newPasswordAgainError.classList.add('show-error');
    }

    else{
        success = true;
        newPasswordError.classList.remove('show-error');
    }

    if(newPassword != newPasswordAgain){
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
        success = true;
        newPasswordError.classList.remove('show-error');
    }

    return success == true;
}
