date = new Date();

password_box = document.querySelector('#password');
error_msg = document.querySelectorAll('.show-error');
password_eye = document.querySelector('.password-eye');

for(em of error_msg){
    em.style.display = 'none';
}

male_div = document.querySelector('#male');
female_div = document.querySelector('#female');
others_div = document.querySelector('#others');

gender_div = [male_div, female_div, others_div];

gender_div.forEach((div) => {
    div.addEventListener('click', () => {
        for(sex_div of gender_div){
            sex_div.classList.remove('selected-gender');
        }

        div.classList.add('selected-gender');
    });
}
);

function validateForm(){
    username_regex = /^[a-z]\w+/i;
    email_regex = /[a-z0-9]+@[a-z]+[.][a-z]/i;
    password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    dob_day = document.querySelector('#dob-day');
    dob_year = document.querySelector('#dob-year');
    dob_month = document.querySelector('#dob-month');

    dob_error = document.querySelector('.dob-error');
    gender_error = document.querySelector('.gender-error');
    username_error = document.querySelector('.username-error');
    password_error = document.querySelector('.password-error');
    email_error = document.querySelector('.signup-email-error');

    password = password_box.value;
    email = document.querySelector('#email').value;
    username = document.querySelector('#username').value;

    dob_day_value = dob_day.value;
    dob_year_value = dob_year.value;
    dob_month_value = dob_month.value;

    if(!username){
        username_error.innerHTML = "Invalid Username";
        username_error.style.display = 'block';
    }

    else if(username.indexOf(' ') != -1){
        username_error.innerHTML = "Username must not contain space(s)";
        username_error.style.display = 'block';
    }

    else if(username_regex.test(username) == false){
        username_error.innerHTML = "Username must start with a letter";
        username_error.style.display = 'block';
    }

    else if(username.length < 4 || username.length > 10){
        username_error.innerHTML = "Username must be 4-10 characters long";
        username_error.style.display = 'block';
    }

    else{
        username_error.style.display = 'none';
    }

    if(email.indexOf('@') != -1 && email.indexOf(' ') != -1){
        email_error.innerHTML = 'Email must not contain spaces(s)';
        email_error.style.display = 'block';
    }

    else if(email_regex.test(email) === false){
        email_error.innerHTML = "Invalid Email";
        email_error.style.display = 'block';
    }

    else{
        email_error.style.display = 'none';
    }

    if(password_regex.test(password) == false){
        password_error.innerHTML = "Password must be a combination of letters, numbers, and special characters, with a minimum length of 8 characters"
        password_error.style.display = 'block';
    }

    else{
        password_error.style.display = 'none';
    }

    if(!dob_day_value || !dob_month_value || !dob_year_value ||
       isNaN(parseInt(dob_day_value)) || isNaN(parseInt(dob_month_value)) || isNaN(parseInt(dob_year_value)) ||
       !(dob_day_value > 0 && dob_day_value < 32) || !(dob_month_value > 0 && dob_month_value < 13) ||
       !(dob_year_value >= 1920 && dob_year_value <= date.getFullYear())){
           dob_error.innerHTML = 'Invalid Date of Birth';
           dob_error.style.display = 'block';
        }

    else{
        dob_error.style.display = 'none';
    }

    selected_gender = '';

    for(genderDiv of gender_div){
        if(genderDiv.classList.contains('selected-gender')){
            selected_gender = genderDiv;
        }
    }

    if(selected_gender){
        gender_error.style.display = 'none';
    }

    else{
        gender_error.innerHTML = 'Select any one';
        gender_error.style.display = 'block';
    }
}

password_eye.addEventListener('click', (event) => {
    if(password_box.type == 'text'){
        password_box.type = 'password';
        password_eye.classList.add('bxs-hide');
        password_eye.classList.remove('bxs-show');
    }

    else{
        password_box.type = 'text';
        password_eye.classList.add('bxs-show');
        password_eye.classList.remove('bxs-hide');
    }
});


password_box.addEventListener('keydown', (event) => {
    values = password_box.value

    if(values.length >= 1){
        if(password_eye.classList.contains('show-hide-password')){
            password_eye.classList.remove('show-hide-password');
        }
    }

    else if(values.length == 0){
        password_eye.classList.add('show-hide-password');
    }
});
