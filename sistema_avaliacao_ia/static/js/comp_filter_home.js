document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.querySelector('.search-bar');
    const allCards = document.querySelectorAll('.competition-card');
    const filterPred = document.getElementById('filter-pred');
    const filterSimul = document.getElementById('filter-simul');
    const filterAll = document.getElementById('filter-all');

    let currentFilter = 'todas';

    function updateFilters() {
        const searchQuery = searchBar.value.toLowerCase();

        allCards.forEach(card => {
            const title = card.dataset.title;
            const type = card.dataset.type;

            const searchMatch = title.includes(searchQuery);
            let filterMatch = false;

            if (currentFilter === 'todas') {
                filterMatch = true;
            } else if (currentFilter === type) {
                filterMatch = true;
            }

            if (searchMatch && filterMatch) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchBar.addEventListener('keyup', updateFilters);
    
    filterPred.addEventListener('click', () => {
        currentFilter = 'predição';
        updateFilters();
    });

    filterSimul.addEventListener('click', () => {
        currentFilter = 'simulação';
        updateFilters();
    });

    filterAll.addEventListener('click', () => {
        currentFilter = 'todas';
        updateFilters();
    });
});