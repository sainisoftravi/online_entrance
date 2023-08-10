menu = document.querySelector('.bx-menu');
close_menu = document.querySelector('.bx-x');
left_container = document.querySelector('.left-container');
right_container = document.querySelector('.right-container');
dashboard_container = document.querySelector('.dashboard-container');


menu.addEventListener('click', (Event) => {
    menu.style.display = 'none';
    close_menu.style.display = 'block';
    left_container.style.width = '100%';
    left_container.style.display = 'flex';
    dashboard_container.style = 'flex-direction:column';
});


close_menu.addEventListener('click', (Event) => {
    menu.style.display = 'block';
    close_menu.style.display = 'none';
    left_container.style.display = 'none';
    dashboard_container.style = 'flex-direction:row';
});
