function validateForm(){
    success = true;
    total_question_error = document.querySelector('.total-questions-error');
    total_question_input_value = document.querySelector('#total-questions').value.trim();

    num_validator = /^\d+$/i;

    if(!num_validator.test(total_question_input_value)){
        success = false;
        total_question_error.classList.add('show-error');
    }

    return success == true;
}
