var remainingTime;
var first_clicked = false;
var timer_div = document.querySelector('.timer');


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

    return true;
}

document.addEventListener("click", () => {
        if(first_clicked == false){
            first_clicked = true;
            const startTime = Date.now();
            const countdownDuration = 2 * 60 * 60 * 1000;

            const endTime = startTime + countdownDuration;
            timer_text = document.querySelector('#timer-text');
            const countdownInterval = setInterval(updateCountdown, 1000);

            function updateCountdown() {
                const currentTime = Date.now();
                const remainingTime = endTime - currentTime;

                if (remainingTime <= 0) {
                    clearInterval(countdownInterval);
                    return true;
                }

                hours = Math.floor(remainingTime / (1000 * 60 * 60));
                minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
                seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

                hours = hours.toString().padStart(2, "0");
                minutes = minutes.toString().padStart(2, "0");
                seconds = seconds.toString().padStart(2, "0");

                timer_text.innerText = `${hours} : ${minutes} : ${seconds}`;

                if(timer_div.style.display == ''){
                    timer_div.style.display = 'block';
                }
            }
        }
    }
);
