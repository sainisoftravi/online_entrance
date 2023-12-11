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

    else if(type_value == "Programme"){
        programme_regex = /^[a-zA-Z]+$/;

        if(programme_regex.test(search_value)){
            error_element.classList.remove('show-error');
        }

        else{
            success = false;
            error_element.innerText = 'Invalid Programme';
            error_element.classList.add('show-error');
        }
    }

    else if(type_value == 'Tests Taken'){
        tests_taken_regex = /[0-9]+/;

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

        if(value == 'Programme'){
            search_by_input.placeholder = 'BCA, BIT, ...';
        }

        else if(value == 'Tests Taken'){
            search_by_input.placeholder = '75, 85, .....';
        }
    });
});
