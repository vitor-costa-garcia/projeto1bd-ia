document.addEventListener('DOMContentLoaded', () => {
    
    const scriptTag = document.getElementById('form-script');
    const minDate = scriptTag ? scriptTag.dataset.serverToday : new Date().toISOString().split('T')[0];

    const dataInicioInput = document.querySelector('input[name="data_inicio"]');
    const dataFimInput = document.querySelector('input[name="data_fim"]');
    
    if (dataInicioInput) {
        dataInicioInput.setAttribute('min', minDate);
    }
    if (dataFimInput) {
        dataFimInput.setAttribute('min', minDate);
    }

    if (dataInicioInput && dataFimInput) {
        dataInicioInput.addEventListener('change', () => {
            const selectedStartDate = dataInicioInput.value;
            
            if (selectedStartDate) {
                dataFimInput.setAttribute('min', selectedStartDate);
                
                if (dataFimInput.value && dataFimInput.value < selectedStartDate) {
                    dataFimInput.value = "";
                }
            } else {
                dataFimInput.setAttribute('min', minDate);
            }
        });
    }

    const simulFormDiv = document.getElementById('simul-form-input');
    const predFormDiv = document.getElementById('pred-form-input');
    const oficialFormDiv = document.getElementById('oficial-form-input');

    const tipoCompFormSelect = document.getElementById('tipo-comp-select');
    const oficialFormSelect = document.getElementById('oficial-select');
    const metricaPredSelect = document.getElementById('metrica_predicao');

    const predInputs = predFormDiv.querySelectorAll('input[type="file"], select');
    const simulInputs = simulFormDiv.querySelectorAll('input[type="file"], select');
    const oficialInputs = oficialFormDiv.querySelectorAll('input, select');

    function ShowPredForm(){
        simulFormDiv.style.display = 'none';
        predFormDiv.style.display = 'block';
        predInputs.forEach(input => input.setAttribute('required', 'required'));
        simulInputs.forEach(input => input.removeAttribute('required'));
        
        if (metricaPredSelect) {
            metricaPredSelect.value = 'RMSE';
        }
    }

    function ShowSimulForm(){
        simulFormDiv.style.display = 'block';
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
            oficialFormDiv.style.display = 'block';
            oficialInputs.forEach(input => input.setAttribute('required', 'required'));
        }
    })

    HideBothForm();
    oficialFormDiv.style.display = 'none';
    oficialInputs.forEach(input => input.removeAttribute('required'));

    const addRuleBtn = document.getElementById('add-rule-btn');
    const removeRuleBtn = document.getElementById('remove-rule-btn');
    const rulesContainer = document.getElementById('rules-container');
    let ruleCounter = 0;

    if (addRuleBtn) {
        addRuleBtn.addEventListener('click', () => {
            ruleCounter++;
            const newRuleInput = document.createElement('div');
            newRuleInput.className = 'form-group rule-item';
            newRuleInput.innerHTML = `
                <input type="text" name="regra" placeholder="Regra #${ruleCounter}" required>
            `;
            rulesContainer.appendChild(newRuleInput);
        });
    }

    if (removeRuleBtn) {
        removeRuleBtn.addEventListener('click', () => {
            if (rulesContainer.children.length > 0) {
                rulesContainer.removeChild(rulesContainer.lastChild);
                if (ruleCounter > 0) ruleCounter--;
            }
        });
    }
});