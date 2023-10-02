bx_x = document.querySelector('.bx-x');
message_div = document.querySelector('.message-div');
error_message = document.querySelector('.error-message');
success_message = document.querySelector('.success-message');

if(error_message || success_message){
    if(bx_x){
        bx_x.addEventListener('click', (Event) => {
            message_div.style.display = 'none';
        });
    }
}
