profile_image = document.querySelector('.profile-img');
drop_down_menu = document.querySelector('.drop-down-menu');

profile_image.addEventListener('click', () => {
    drop_down_menu.classList.toggle('open-menu');
})

document.addEventListener('click', function (event) {
    if(event.target.matches('.profile-img') == false){
        drop_down_menu.classList.remove('open-menu');
    }
    }
);
