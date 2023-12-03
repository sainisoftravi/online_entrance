window.addEventListener('load', () => {
    bx_x = document.querySelector('.bx-x');
    select = document.querySelector('#rank-by');
    form = document.querySelector('#rank-by-form');
    rank_div = document.querySelector('.rank-system-info');

    bx_x.addEventListener('click', () => {
        rank_div.style.display = 'none';
    });

    select.addEventListener('change', () => {
        form.submit();
    })
});
