const comp_cards = document.getElementsByClassName("competition-card")

function HidePredShowSimul(){
    for(let i = 0; i < comp_cards.length; i++){
        if(comp_cards[i].id%2==0){
            comp_cards[i].style.display = '';
        } else {
            comp_cards[i].style.display = 'none';
        }
    }
}

function HideSimulShowPred(){
    for(let i = 0; i < comp_cards.length; i++){
        if(comp_cards[i].id%2==1){
            comp_cards[i].style.display = '';
        } else {
            comp_cards[i].style.display = 'none';
        }
    }
}

function ClearFilter(){
    for(let i = 0; i < comp_cards.length; i++){
        comp_cards[i].style.display = '';
    }
}