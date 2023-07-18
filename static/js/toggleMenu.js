menu = document.querySelector('.bx-menu');
close_menu = document.querySelector('.bx-x');
left_container = document.querySelector('.left-container');


menu.addEventListener('click', (Event) => {
    menu.style.display = 'none';
    close_menu.style.display = 'block';
    left_container.style.display = 'flex';
});


close_menu.addEventListener('click', (Event) => {
    menu.style.display = 'block';
    close_menu.style.display = 'none';
    left_container.style.display = 'none';
});
