const simulFormDiv = document.getElementById('simul-form-input');
const predFormDiv = document.getElementById('pred-form-input');
const oficialFormDiv = document.getElementById('oficial-form-input');

const tipoCompFormSelect = document.getElementById('tipo-comp-select');
const oficialFormSelect = document.getElementById('oficial-select');

const predInputs = predFormDiv.querySelectorAll('input[type="file"], select');
const simulInputs = simulFormDiv.querySelectorAll('input[type="file"], select');
const oficialInputs = oficialFormDiv.querySelectorAll('input, select');

function ShowPredForm(){
    simulFormDiv.style.display = 'none';
    predFormDiv.style.display = '';
    predInputs.forEach(input => input.setAttribute('required', 'required'));
    simulInputs.forEach(input => input.removeAttribute('required'));
}

function ShowSimulForm(){
    simulFormDiv.style.display = '';
    predFormDiv.style.display = 'none';
    simulInputs.forEach(input => input.setAttribute('required', 'required'));
    predInputs.forEach(input => input.removeAttribute('required'));
};

function HideBothForm(){
    simulFormDiv.style.display = 'none';
    predFormDiv.style.display = 'none';
    predInputs.forEach(input => input.removeAttribute('required'));
    simulInputs.forEach(input => input.removeAttribute('required'));
};

tipoCompFormSelect.addEventListener('change', () => {
    HideBothForm()
    if(tipoCompFormSelect.value === '0'){
        ShowPredForm()
    } else if (tipoCompFormSelect.value === '1') {
        ShowSimulForm();
    }
})

oficialFormSelect.addEventListener('change', () => {
    oficialFormDiv.style.display = 'none';
    oficialInputs.forEach(input => input.removeAttribute('required'));
    
    if(oficialFormSelect.value === '1'){ 
        oficialFormDiv.style.display = '';
        oficialInputs.forEach(input => input.setAttribute('required', 'required'));
    }
})

HideBothForm();
oficialFormDiv.style.display = 'none';
oficialInputs.forEach(input => input.removeAttribute('required'));