var selectedFile;
var input = document.querySelector("#upload-profile-button");
var profile_image_error = document.querySelector('.profile-image-error');
input.addEventListener('change', updateImageDisplay);


function updateImageDisplay() {
    imageExtension = ['jpg', 'jpeg', 'png']
    extension = input.files[0]['name'].split('.')[1]

    if(!imageExtension.includes(extension)){
        input.value = null;
    }

    if(input.files.length != 0){
        document.querySelector('.user-image').src = window.URL.createObjectURL(input.files[0])
    }

    if(input.files.length == 0) {
        input.files = selectedFile;
        profile_image_error.classList.add('show-error');

        setTimeout(function() {
            $(profile_image_error).removeClass('show-error');

        }, 2000);
    }

    else {
        selectedFile = input.files;
        profile_image_error.classList.remove('show-error');
   }
}


function validateForm(){
    success = true;
    emailRegex = /[a-z0-9]+@[a-z]+[.][a-z]/i;

    emailArea = document.getElementById('Email');
    genderArea = document.getElementById('Gender');
    dobArea = document.getElementsByName('DOB')[0];
    memberSinceArea = document.getElementById('Member Since');

    dobError = document.querySelector('.DOB-error');
    emailError = document.querySelector('.Email-error');
    genderError = document.querySelector('.Gender-error');

    emailValue = emailArea.value.trim();
    genderValue = genderArea.value.trim();

    if(!emailValue){
        success = false;
        emailError.classList.add('show-error');
        emailError.innerText = 'This field must not be empty';
    }

    else if(!emailRegex.test(emailValue)){
        success = false;
        emailError.classList.add('show-error');
        emailError.innerText = 'Invalid Email';
    }

    else{
        emailError.classList.remove('show-error');
    }

    if(is_superuser == false){
        if(!genderValue){
            success = false;
            genderError.classList.add('show-error');
            genderError.innerText = 'This field must not be empty';
        }

        else if(['male', 'female'].indexOf(genderValue.toLowerCase()) == -1){
            success = false;
            genderError.classList.add('show-error');
            genderError.innerText = 'Gender must be either: Male or Female';
        }

        else{
            genderError.classList.remove('show-error');
        }

        currentDate = new Date();
        currentYear = currentDate.getFullYear();
        minYear = currentYear - 100;
        maxYear = currentYear - 15;
        formYear = dobArea.value.split('-')[0];

        if(formYear < minYear || formYear > maxYear){
            success = false;
            dobError.classList.add('show-error');
            dobError.innerText = `Date must be in between: 01 Jan ${minYear} - 31 Dec ${maxYear}`;
        }

        else{
            dobError.classList.remove('show-error');
        }
    }

    return success == true;
}
