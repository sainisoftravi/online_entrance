var remainingTime;
var choice_divs = document.getElementsByClassName('choice');
var wrong_div = document.getElementsByClassName('wrong-div');
var submit_button = document.querySelector('#submit-button');
var correct_div = document.getElementsByClassName('correct-div');
var radio_buttons = document.getElementsByClassName('radio-choices');
var option_labels = document.getElementsByClassName('option-labels');


if(wrong_div.length > 0 || correct_div.length > 0){
    for(radio of radio_buttons){
        radio.disabled = true;
    }

    for(choice_div of choice_divs){
        choice_div.style.cursor = 'not-allowed';
    }

    for(option_label of option_labels){
        option_label.style.cursor = 'not-allowed'
    }
}

function showErrorMessage(){
    scrolled = false;
    questionsDivs = document.getElementsByClassName('Questions');

    for(radio_counter=1; radio_counter <= 100; radio_counter++){
        questionDiv = questionsDivs[radio_counter - 1];
        error_message = questionDiv.getElementsByClassName('error-message')[0];

        if(isAllRadioButtonsSelected(radio_counter)){
            if(scrolled == false){
                scrolled = true;
                questionDiv.scrollIntoView()
            }

            error_message.classList.add('show-error-message');
        }

        else{
            error_message.classList.remove('show-error-message');
        }
    }
}

function isAllRadioButtonsSelected(radio_counter){
    not_selected = 0;

    for(radios of document.getElementsByName(`choices ${radio_counter}`)){
        if(radios.checked == false){
            not_selected += 1;
        }
    }

    return not_selected == 4;
}

function checkForSubmission(){
    isFinished = true;

    if (remainingTime <= 0){
        isFinished = true;
    }

    else{
        for(radio_counter=1; radio_counter <= 100; radio_counter++){
            if(isAllRadioButtonsSelected(radio_counter) == true){
                isFinished = false;
                break
            }
        }

        if(isFinished == false){
            showErrorMessage();
            return false;
        }
    }

    return isFinished;
}


window.addEventListener("load", () => {
    priorDuration = 5 * 1000;
    priorEndTime = Date.now() + priorDuration;

    examEndTime = 0;
    examCountDownDuration = 0;
    examCountDownInterval = 0;

    timer_text = document.querySelector('#timer-text');

    if(timer_text){
        priorCountDownInterval = setInterval(priorTime, 50);
    }

    function priorTime(){
        remainingTime = priorEndTime - Date.now();
        seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

        if(remainingTime <= 1300){
            clearInterval(priorCountDownInterval);

            examCountDownDuration = 2 * 60 * 60 * 1000;
            examEndTime = Date.now() + examCountDownDuration + 1000;
            examCountDownInterval = setInterval(startExamTime, 50);
        }

        else{
            timer_text.innerText = `Starts at: ${seconds}`;
        }
    }

    function startExamTime() {
        remainingTime = examEndTime - Date.now();

        if (remainingTime <= 0) {
            clearInterval(examCountDownInterval);
            submit_button.click();
            return true;
        }

        hours = Math.floor(remainingTime / (1000 * 60 * 60));
        minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

        hours = hours.toString().padStart(2, "0");
        minutes = minutes.toString().padStart(2, "0");
        seconds = seconds.toString().padStart(2, "0");

        timer_text.innerText = `${hours} : ${minutes} : ${seconds}`;
    }
});
