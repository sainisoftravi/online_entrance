changeProfileForm = document.getElementById('changeProfileForm');
successMessageDiv = document.querySelector('.success-message-div');
changeProfileButton = document.getElementById('changeProfileButton');
var profile_image_error = document.querySelector('.profile-image-error');


setTimeout(function() {
    $(successMessageDiv).fadeOut('fast');
}, 1500);


changeProfileButton.addEventListener('change', () => {
    imageExtension = ['jpg', 'jpeg', 'png'];
    extension = changeProfileButton.files[0]['name'].split('.')[1];

    if(!imageExtension.includes(extension)){
        changeProfileButton.value = null;
        profile_image_error.classList.add('show-error');

        setTimeout(function() {
            $(profile_image_error).removeClass('show-error');

        }, 2000);
    }

    if(changeProfileButton.files.length != 0){
        changeProfileForm.submit();
        profile_image_error.classList.remove('show-error');
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
        success = true;
        newPasswordError.classList.remove('show-error');
    }

    return success == true;
}
