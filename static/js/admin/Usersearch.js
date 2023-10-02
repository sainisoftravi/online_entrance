function validateForm(){
    success = true;
    type_value = search_by_select.value.trim();
    search_value = search_by_input.value.trim();

    if(search_value.length == 0){
        success = false;
        error_element.innerText = 'Search value must not be empty';
        error_element.classList.add('show-error');
    }

    else if(type_value == "Search by"){
        success = false;
        error_element.innerText = 'Select any option in Search By drop-down';
        error_element.classList.add('show-error');
    }

    else if(type_value == "Email"){
        email_regex = /[a-z0-9]+@[a-z]+[.][a-z]+/i

        if(email_regex.test(search_value)){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Invalid Email Address';
            error_element.classList.add('show-error');
        }
    }

    else if(type_value == "DOB" || type_value == "Member Since"){
        dob_regex = /^(?:19|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;

        if(dob_regex.test(search_value)){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Date must be in YYYY-MM-DD form';
            error_element.classList.add('show-error');
        }
    }

    else if(type_value == "Gender"){
        genders = ['male', 'm', 'female', 'f', 'others', 'other', 'o'];

        if(genders.includes(search_value.toLowerCase())){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Invalid Gender. Gender should be: Male(m), Female(f) or Others(o)';
            error_element.classList.add('show-error');
        }
    }

    return success == true;
}

window.onload = () => {
    search_by_select = document.querySelector("#search-by");
    error_element = document.querySelector('.error-message');
    searching_form = document.querySelector('#searching-form');
    search_by_input = document.querySelector('#search-by-input');

    search_by_select.addEventListener('change', function(event){
        value = search_by_select.value;

        if(value == 'Email'){
            search_by_input.placeholder = 'xyz@xyz.com';
        }

        else if(value == 'DOB' || value == 'Member Since'){
            search_by_input.placeholder = 'YYYY-MM-DD';
        }

        else if(value == 'Gender'){
            search_by_input.placeholder = 'M or F';
        }

        else if(['Admin', 'Active', 'Non-Active', 'Non-Admin'].includes(value)){
            event.preventDefault();
            searching_form.submit();
        }
    });
}
