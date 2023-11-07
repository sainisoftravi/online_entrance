profile_image = document.querySelector('.profile-img');
detached_pop_up_menu = document.querySelector('.detached-pop-up');

if(profile_image){
    profile_image.addEventListener('click', () => {
        if(detached_pop_up_menu.classList.contains('hide')){
            detached_pop_up_menu.classList.remove('hide');
        }

        else{
            detached_pop_up_menu.classList.add('hide');
        }
    });


    document.addEventListener('click', (Event) => {
        element = Event.target;

        if(element != detached_pop_up_menu && element != profile_image){
            detached_pop_up_menu.classList.add('hide');
        }
    });
}
