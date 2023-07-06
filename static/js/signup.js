date = new Date();

password_box = document.querySelector('#password');
error_msg = document.querySelectorAll('.show-error');

for(em of error_msg){
    em.classList.remove('show-error');
}

male_div = document.querySelector('.male-div');
female_div = document.querySelector('.female-div');
others_div = document.querySelector('.others-div');

male_radio = document.querySelector('#male');
female_radio = document.querySelector('#female');
others_radio = document.querySelector('#others');

gender_div = [male_div, female_div, others_div];

gender_div.forEach((div) => {
    div.addEventListener('click', () => {
        for(sex_div of gender_div){
            sex_div.classList.remove('selected-gender');
        }

        if(div == male_div){
            male_radio.checked = true;
        }

        else if(div == female_div){
            female_radio.checked = true;
        }

        if(div == others_div){
            others_radio.checked = true;
        }

        div.classList.add('selected-gender');
    });
}
);


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


function validateForm(){
    success = true;
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;
    password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    dob_day = document.querySelector('#dob-day');
    dob_year = document.querySelector('#dob-year');
    dob_month = document.querySelector('#dob-month');

    dob_error = document.querySelector('.dob-error');
    gender_error = document.querySelector('.gender-error');
    password_error = document.querySelector('.password-error');
    email_error = document.querySelector('.signup-email-error');

    password = password_box.value;
    email = document.querySelector('#email').value;

    dob_day_value = dob_day.value;
    dob_year_value = dob_year.value;
    dob_month_value = dob_month.value;

    if(email.indexOf('@') != -1 && email.indexOf(' ') != -1){
        success = false;
        email_error.classList.add('show-error');
        email_error.innerText = 'Email must not contain spaces(s)';
    }

    else if(email_regex.test(email) === false){
        success = false;
        email_error.classList.add('show-error');
        email_error.innerText = "Invalid Email";
    }

    else{
        email_error.classList.remove('show-error');
    }

    if(password_regex.test(password) == false){
        success = false;
        password_error.classList.add('show-error');
        password_error.innerText = "Password must be a combination of letters, numbers, and special characters, with a minimum length of 8 characters"
    }

    else{
        password_error.classList.remove('show-error');
    }

    if(!dob_day_value || !dob_month_value || !dob_year_value ||
       isNaN(parseInt(dob_day_value)) || isNaN(parseInt(dob_month_value)) || isNaN(parseInt(dob_year_value)) ||
       !(dob_day_value > 0 && dob_day_value < 32) || !(dob_month_value > 0 && dob_month_value < 13) ||
       !(dob_year_value >= 1920 && dob_year_value <= date.getFullYear())){
           success = false;
           dob_error.classList.add('show-error');
           dob_error.innerText = 'Invalid Date of Birth';
        }

    else{
        dob_error.classList.remove('show-error');
    }

    selected_gender = '';

    for(genderDiv of gender_div){
        if(genderDiv.classList.contains('selected-gender')){
            selected_gender = genderDiv;
        }
    }

    if(selected_gender){
        gender_error.classList.remove('show-error');
    }

    else{
        success = false;
        gender_error.classList.add('show-error');
        gender_error.innerText = 'Select any one';
    }

    return success == true;
}
