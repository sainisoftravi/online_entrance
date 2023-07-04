program_divs = document.getElementsByClassName('program');
get_program_input = document.querySelector('#get_program');

get_program_input.addEventListener('input', () => {
    from_input = get_program_input.value.toLowerCase();

    for(program_div of program_divs){
        if(program_div.text.toLowerCase().startsWith(from_input)){
            program_div.style.display = 'block';
        }

        else{
            program_div.style.display = 'none';
        }
    }
});
