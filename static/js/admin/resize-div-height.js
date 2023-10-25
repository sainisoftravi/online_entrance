window.onload = function() {
    if(window.screen.width > 600){
        var divs = document.getElementsByClassName('inner-wrapper');
        var maxHeight = 0;

        for (var i = 0; i < divs.length; i++) {
            if (divs[i].clientHeight > maxHeight) {
                maxHeight = divs[i].clientHeight;
            }
        }

        for (var i = 0; i < divs.length; i++) {
            divs[i].style.height = maxHeight + "px";
        }
    }
};
