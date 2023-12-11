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

    else if(type_value == 'Username'){
        username_regex = /^[a-zA-Z0-9_ \u4e00-\u9fa5\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\u1100-\u11FF\uAC00-\uD7A3]+$/i;

        if(username_regex.test(search_value)){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Invalid Username. Username must container letter and spaces only';
            error_element.classList.add('show-error')
        }
    }

    else if(type_value == 'Tests Taken'){
        tests_taken_regex = /^[0-9]+$/;

        if(tests_taken_regex.test(search_value)){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Tests Taken must be number';
            error_element.classList.add('show-error')
        }
    }

    return success == true;
}

window.addEventListener('load', function() {
    search_by_select = document.querySelector("#search-by");
    error_element = document.querySelector('.error-message');
    searching_form = document.querySelector('#searching-form');
    search_by_input = document.querySelector('#search-by-input');

    search_by_select.addEventListener('change', function(event){
        value = search_by_select.value;

        if(value == 'Email'){
            search_by_input.placeholder = 'xyz@xyz.com';
        }

        else if(value == 'Username'){
            search_by_input.placeholder = 'John Doe';
        }

        else if(value == 'Tests Taken'){
            search_by_input.placeholder = '75, 85, .....';
        }
    });
});
