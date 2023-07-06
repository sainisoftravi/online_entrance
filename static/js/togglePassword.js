password_box1 = document.getElementsByName('new_password1')[0];
password_box2 = document.getElementsByName('new_password2');
password_eye1 = document.getElementsByClassName('pass-eye1')[0];
old_password_box = document.getElementsByName('old_password');

password_eyes = [password_eye1]
password_boxes = [password_box1];

if(old_password_box.length > 0){
    password_boxes.push(old_password_box[0])

    password_eye0 = document.getElementsByClassName('pass-eye0')[0];
    password_eyes.push(password_eye0)
}

if(password_box2.length > 0){
    password_eye2 = document.getElementsByClassName('pass-eye2')[0];

    password_boxes.push(password_box2[0])
    password_eyes.push(password_eye2)
}

password_eyes.forEach((password_eye, index) => {
    password_eye.addEventListener('click', (event) => {
        if(password_boxes[index].type == 'text'){
            password_boxes[index].type = 'password';
            password_eye.classList.remove('bxs-show');
            password_eye.classList.add('bxs-hide');
        }

        else{
            password_boxes[index].type = 'text';
            password_eye.classList.add('bxs-show');
            password_eye.classList.remove('bxs-hide');
        }
    });
});


password_boxes.forEach((password_box, index) => {
    password_box.addEventListener('input', (event) => {
        values = password_box.value

        if(values.length >= 1){
            if(!password_eyes[index].classList.contains('show-eye')){
                password_eyes[index].classList.add('show-eye');
                password_eyes[index].classList.remove('bxs-show');
            }
        }

        else if(values.length == 0){
            password_eyes[index].classList.remove('show-eye');
        }
    });
});
