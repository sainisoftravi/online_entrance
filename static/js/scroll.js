const toTop = document.querySelector('.go-to-top');

window.addEventListener('scroll', scroll);

function scroll(){
    if(window.scrollY > 50){
        toTop.classList.add('active');

        pos = document.documentElement.scrollTop;
        calcHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        scrollValue = Math.round((pos * 100) / calcHeight);

        toTop.style.background = `conic-gradient(#03cc65 ${scrollValue}%, #d7d7d7 ${scrollValue}%)`;
    }

    else{
        toTop.classList.remove('active');
    }
}
