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

    else if(type_value == "User"){
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

    else if(type_value == 'Total Questions To Select'){
        validator = /^-?[\d.]+(?:e-?\d+)?$/

        if(validator.test(search_value)){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Number was expected';
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

        if(value == 'Programme Name'){
            search_by_input.placeholder = 'BCA, BIT, BIM ...';
        }

        else if(value == 'Subject Name'){
            search_by_input.placeholder = 'English, Math, ...';
        }

        else if(value == 'Total Questions To Select'){
            search_by_input.placeholder = 'Any number';
        }
    });
}
