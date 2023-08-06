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
