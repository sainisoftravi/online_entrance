logout_div = document.querySelector('.logout-link');
logout_link = document.querySelector('.logout-link');
profile_image = document.querySelector('.profile-img');

if(profile_image){
    profile_image.addEventListener('mouseover', () => {
        logout_div.classList.add('show-logout-link');
        logout_div.classList.remove('hide-logout-link');
    });


    document.addEventListener('click', (Event) => {
        if(Event.target != logout_link){
            logout_div.classList.remove('show-logout-link');
            logout_div.classList.add('hide-logout-link');
        }
    });
}
