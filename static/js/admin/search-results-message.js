window.addEventListener('load', () => {
    search_result_x = document.querySelector('.bx-x');

    if(search_result_x){
        search_info_div = document.querySelector('.searched_number');

        search_result_x.addEventListener('click', (event)=>{
            $(search_info_div).fadeOut('fast');
        });
    }
})
