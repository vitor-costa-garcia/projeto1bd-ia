const simulFormDiv = document.getElementById('simul-form-input')
const predFormDiv = document.getElementById('pred-form-input')
const oficialFormDiv = document.getElementById('oficial-form-input');

const tipoCompFormSelect = document.getElementById('tipo-comp-select')
const oficialFormSelect = document.getElementById('oficial-select')

function ShowPredForm(){
    simulFormDiv.style.display = 'none';
    predFormDiv.style.display = '';
}

function ShowSimulForm(){
    simulFormDiv.style.display = '';
    predFormDiv.style.display = 'none';
};

function HideBothForm(){
    simulFormDiv.style.display = 'none';
    predFormDiv.style.display = 'none';
};

tipoCompFormSelect.addEventListener('change', () => {
    HideBothForm()
    if(tipoCompFormSelect.value === '0'){
        ShowPredForm()
    } else {
        ShowSimulForm();
    }
})

oficialFormSelect.addEventListener('change', () => {
    oficialFormDiv.style.display = 'none';
    if(oficialFormSelect.value === '0'){
        oficialFormDiv.style.display = ''
    }
})