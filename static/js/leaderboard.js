window.addEventListener('load', () => {
    bx_x = document.querySelector('.bx-x');
    select = document.querySelector('#rank-by');
    form = document.querySelector('#rank-by-form');
    rank_div = document.querySelector('.rank-system-info');

    if(bx_x){
        bx_x.addEventListener('click', () => {
            $(rank_div).fadeOut(500);
        });
    }

    select.addEventListener('change', () => {
        form.submit();
    })
});
