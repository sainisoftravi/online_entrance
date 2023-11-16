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
            search_by_input.placeholder = 'BCA, BIT, BIM ...';
        }

        else if(value == 'Subject'){
            search_by_input.placeholder = 'English, Math, ...';
        }

        else if(value == 'Title'){
            search_by_input.placeholder = 'Title of Question';
        }

        else if(value == 'Answer'){
            search_by_input.placeholder = 'Answer';
        }

        else if(value == 'Options'){
            search_by_input.placeholder = 'Options';
        }
    });
});
