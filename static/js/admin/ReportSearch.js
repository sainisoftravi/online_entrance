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

    return success == true;
}

window.addEventListener('load', function() {
    search_by_select = document.querySelector("#search-by");
    error_element = document.querySelector('.error-message');
    searching_form = document.querySelector('#searching-form');
    search_by_input = document.querySelector('#search-by-input');

    if(search_by_select){
        search_by_select.addEventListener('change', function(event){
            value = search_by_select.value;

            if(value == 'User'){
                search_by_input.placeholder = 'xyz@xyz.com';
            }

            else if(value == 'Issue'){
                search_by_input.placeholder = 'Issue';
            }

            else if(value == 'Date'){
                search_by_input.placeholder = 'YYYY-MM-DD';
            }

            else if(value == 'Question'){
                search_by_input.placeholder = 'Question';
            }

            else if(['Marked', 'Not-Marked'].includes(value)){
                searching_form.submit()
            }
        });
    }
});
