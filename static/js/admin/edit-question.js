function validateForm(){
    success = true;

    titleAreaValue = document.querySelector('#Title').value.trim();
    answerAreaValue = document.querySelector('#Answer').value.trim();
    oneAreaValue = document.getElementById('Option One').value.trim();
    twoAreaValue = document.getElementById('Option Two').value.trim();
    fourAreaValue = document.getElementById('Option Four').value.trim();
    threeAreaValue = document.getElementById('Option Three').value.trim();
    subjectValue = document.querySelector('#subject-select').value.trim();
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

    if(!titleAreaValue){
        success = false;
        titleError.classList.add('show-error');
    }

    else{
        titleError.classList.remove('show-error');
    }

    if(!answerAreaValue){
        success = false;
        answerError.classList.add('show-error');
    }

    else{
        answerError.classList.remove('show-error');
    }

    if(!oneAreaValue){
        success = false;
        oneError.classList.add('show-error');
    }

    else{
        oneError.classList.remove('show-error');
    }

    if(!twoAreaValue){
        success = false;
        twoError.classList.add('show-error');
    }

    else{
        twoError.classList.remove('show-error');
    }

    if(!threeAreaValue){
        success = false;
        threeError.classList.add('show-error');
    }

    else{
        threeError.classList.remove('show-error');
    }

    if(!fourAreaValue){
        success = false;
        fourError.classList.add('show-error');
    }

    else{
        fourError.classList.remove('show-error');
    }

    if(![oneAreaValue, twoAreaValue, fourAreaValue, threeAreaValue].includes(answerAreaValue)){
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
    select_element = document.querySelector('#programme-select');

    for(select_option in select_options){
        newOption = document.createElement("option");
        newOption.text = select_option;

        select_element.add(newOption);
    }
};
