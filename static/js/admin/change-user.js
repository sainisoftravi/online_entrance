var selectedFile;
var input = document.querySelector("#upload-profile-button");
input.addEventListener('change', updateImageDisplay);

function updateImageDisplay() {
    if(input.files.length != 0){
        document.querySelector('.user-image').src = window.URL.createObjectURL(input.files[0])
    }

    if(input.files.length==0) {
        input.files = selectedFile;
   }

   else {
       selectedFile = input.files;
   }
}
