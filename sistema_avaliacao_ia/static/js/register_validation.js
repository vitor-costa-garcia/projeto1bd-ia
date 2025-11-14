const today = new Date();

const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0');
const dd = String(today.getDate()).padStart(2, '0');
const maxDate = `${yyyy}-${mm}-${dd}`;

document.addEventListener('DOMContentLoaded', () => {
    const dobInput = document.querySelector('input[name="datanascimento"]');
    if (dobInput) {
        dobInput.setAttribute('max', maxDate);
    }
});