function validateForm(){
    success = true;

    titleAreaValue = document.querySelector('#Title').value.trim();
    answerAreaValue = document.querySelector('#Answer').value.trim();
    oneAreaValue = document.getElementById('Option One').value.trim();
    twoAreaValue = document.getElementById('Option Two').value.trim();
    threeAreaValue = document.getElementById('Option Three').value.trim();
    fourAreaValue = document.getElementById('Option Four').value.trim();

    oneError = document.querySelector('.one-error');
    twoError = document.querySelector('.two-error');
    fourError = document.querySelector('.four-error');
    titleError = document.querySelector('.Title-error');
    threeError = document.querySelector('.three-error');
    answerError = document.querySelector('.Answer-error');

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

    return success == true;
}
