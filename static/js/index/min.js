const toTop = document.querySelector('.go-to-top');

window.addEventListener('scroll', function(){
    if(window.scrollY > 50){
        toTop.classList.add('active');
    }

    else{
        toTop.classList.remove('active');
    }
});

// login_button = document.querySelector('#login');

// form_close_button = document.querySelector('.form-close-button');
// login_signup_container = document.querySelector('.login-signup-container');
// login_signup_container.classList.add('form-hide');

// form_close_button.addEventListener('click', () => {
//     login_signup_container.classList.add('form-hide');
// })

// login_button.addEventListener('click', () => {
//     login_signup_container.classList.remove('form-hide');
// })

// login_toggle_button = document.querySelector('.login-toggle-button');
// signup_toggle_button = document.querySelector('.signup-toggle-button');
// const login_form = document.querySelector('.login-form-container');
// const signup_form = document.querySelector('.signup-form-container');
// signup_form.classList.add('form-hide');

// login_toggle_button.addEventListener('click', () => {
//     login_form.classList.remove('form-hide');
//     signup_form.classList.add('form-hide');

//     login_toggle_button.style = 'background: #101b4f; color: whitesmoke;'
//     signup_toggle_button.style = 'background: whitesmoke; color: black;'
// });

// signup_toggle_button.addEventListener('click', () => {
//     login_form.classList.add('form-hide');
//     signup_form.classList.remove('form-hide');

//     login_toggle_button.style = 'background: whitesmoke; color: black;'
//     signup_toggle_button.style = 'background: #101b4f; color: whitesmoke;'
// });

// date = new Date();

// daySelect = document.querySelector('#select-dates');
// monthSelect = document.querySelector('#select-months');
// monthSelect[date.getMonth()].selected = "selected"
// daySelect[date.getDate() - 1].selected = "selected"

// male_div = document.querySelector('.male');
// female_div = document.querySelector('.female');
// others_div = document.querySelector('.others');

// gender_divs = [male_div, female_div, others_div]

// gender_divs.forEach((div) => {
//     div.addEventListener('click', () => {
//         for(sex_div of gender_divs){
//             sex_div.classList.remove('sex-show-border');
//         }

//         div.classList.add('sex-show-border');
//     });
// }
// );
