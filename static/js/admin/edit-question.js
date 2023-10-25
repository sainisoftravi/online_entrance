function validateForm(){
    success = true;

    titleValue = document.querySelector('#Title').value.trim();
    answerValue = document.getElementsByName('Answer')[0].value.trim();
    optionOneValue = document.getElementById('Option One').value.trim();
    optionTwoValue = document.getElementById('Option Two').value.trim();
    optionFourValue = document.getElementById('Option Four').value.trim();
    subjectValue = document.querySelector('#subject-select').value.trim();
    optionThreeValue = document.getElementById('Option Three').value.trim();
    programmeValue = document.querySelector('#programme-select').value.trim();

    oneError = document.querySelector('.one-error');
    twoError = document.querySelector('.two-error');
    fourError = document.querySelector('.four-error');
    titleError = document.querySelector('.Title-error');
    threeError = document.querySelector('.three-error');
    answerError = document.querySelector('.Answer-error');
    subjectError = document.querySelector('.subject-error');
    programmeError = document.querySelector('.programme-error');

    if(programmeValue == "Select Programme"){
        success = false;
        programmeError.classList.add('show-error');
    }

    else{
        programmeError.classList.remove('show-error');
    }

    if(subjectValue == "Select Subject"){
        success = false;
        subjectError.classList.add('show-error');
    }

    else{
        subjectError.classList.remove('show-error');
    }

    if(!titleValue){
        success = false;
        titleError.classList.add('show-error');
    }

    else{
        titleError.classList.remove('show-error');
    }

    if(!answerValue){
        success = false;
        answerError.classList.add('sho-error');
    }

    else{
        answerError.classList.remove('sho-error');
    }

    if(!optionOneValue){
        success = false;
        oneError.classList.add('show-error');
    }

    else{
        oneError.classList.remove('show-error');
    }

    if(!optionTwoValue){
        success = false;
        twoError.classList.add('show-error');
    }

    else{
        twoError.classList.remove('show-error');
    }

    if(!optionThreeValue){
        success = false;
        threeError.classList.add('show-error');
    }

    else{
        threeError.classList.remove('show-error');
    }

    if(!optionFourValue){
        success = false;
        fourError.classList.add('show-error');
    }

    else{
        fourError.classList.remove('show-error');
    }

    if(![optionOneValue, optionTwoValue, optionFourValue, optionThreeValue].includes(answerValue)){
        success = false;
        answerError.innerText = 'Answer must be within the given options'
        answerError.classList.add('show-error');
    }

    else{
        answerError.classList.remove('show-error');
    }

    return success == true;
}


function onSubjectChange(){
    subject_element = document.querySelector('#subject-select');

    for(option of subject_element.options){
        if(option.text == 'Select Subjects'){
            subject_element.removeChild(option);
            break;
        }
    }
}


function onProgrammeChange(){
    subject_element = document.querySelector('#subject-select');
    default_element = document.querySelector("#programme-default");
    program_element = document.querySelector("#programme-select").value;

    while (subject_element.options.length > 0){
        subject_element.remove(0);
    }

    newOption = document.createElement('option');
    newOption.text = 'Select Subjects';
    subject_element.add(newOption);

    if(program_element != "Select Programme"){
        if(default_element){
            default_element.remove();
        }

        subjects = select_options[program_element];

        for(subject of subjects){
            newOption = document.createElement('option');
            newOption.text = subject;

            subject_element.add(newOption);
        }
    }
}

window.onload = function(){
    select_element = document.getElementById('programme-select');

    if(select_element){
        for(select_option in select_options){
            newOption = document.createElement("option");
            newOption.text = select_option;

            select_element.add(newOption);
        }
    }
};
