document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('user-search-input');
    const resultsDiv = document.getElementById('search-results');
    const selectedDiv = document.getElementById('selected-members');
    const form = document.getElementById('team-form');
    const currentUserId = form.dataset.currentUserId;
    
    let addedUserIds = new Set();
    
    function addMemberToForm(id, name) {
        if (addedUserIds.has(id)) return;
        
        addedUserIds.add(id);

        const pill = document.createElement('div');
        pill.className = 'member-pill';
        pill.innerHTML = `
            ${name}
            <button type="button" class="remove-user-btn" data-id="${id}">&times;</button>
        `;
        
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'members';
        hiddenInput.value = id;
        hiddenInput.id = `member-input-${id}`;
        
        form.appendChild(hiddenInput);
        selectedDiv.appendChild(pill);
    }

    searchInput.addEventListener('keyup', async (e) => {
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            resultsDiv.innerHTML = '';
            resultsDiv.style.display = 'none';
            return;
        }

        const response = await fetch(`/api/user/search-users/?q=${query}&exclude=${currentUserId}`);
        const data = await response.json();
        
        resultsDiv.innerHTML = '';
        if (data.users.length > 0) {
            resultsDiv.style.display = 'block';
            data.users.forEach(user => {
                const [id, name] = user;
                if (!addedUserIds.has(String(id))) {
                    const item = document.createElement('div');
                    item.className = 'result-item';
                    item.innerHTML = `
                        <span>${name}</span>
                        <button type="button" class="add-user-btn" data-id="${id}" data-name="${name}">Adicionar</button>
                    `;
                    resultsDiv.appendChild(item);
                }
            });
        } else {
            resultsDiv.style.display = 'none';
        }
    });

    resultsDiv.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-user-btn')) {
            const id = e.target.dataset.id;
            const name = e.target.dataset.name;
            addMemberToForm(id, name);
            e.target.closest('.result-item').remove();
            
            if (resultsDiv.children.length === 0) {
                resultsDiv.style.display = 'none';
            }
        }
    });

    selectedDiv.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-user-btn')) {
            const id = e.target.dataset.id;
            
            addedUserIds.delete(id);
            
            const hiddenInput = document.getElementById(`member-input-${id}`);
            if (hiddenInput) {
                hiddenInput.remove();
            }
            
            e.target.closest('.member-pill').remove();
            
            searchInput.dispatchEvent(new Event('keyup'));
        }
    });
});