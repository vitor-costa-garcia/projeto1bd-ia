document.addEventListener('DOMContentLoaded', () => {
    const compId = document.getElementById('team-management-pod').dataset.compid;
    const equipeId = document.getElementById('team-management-pod').dataset.equipeid;
    const currentUserId = document.getElementById('team-management-pod').dataset.currentuserid;
    const searchInput = document.getElementById('team-user-search');
    const resultsDiv = document.getElementById('team-search-results');
    const memberList = document.getElementById('team-member-list');
    
    const getCsrfToken = () => document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const addedUserIds = new Set();
    document.querySelectorAll('.remove-member-btn').forEach(btn => {
        addedUserIds.add(btn.dataset.userid);
    });

    async function handleSearch(query) {
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
                    item.className = 'team-result-item';
                    item.innerHTML = `
                        <span>${name}</span>
                        <button type="button" class="add-member-btn" data-id="${id}" data-name="${name}">Add</button>
                    `;
                    resultsDiv.appendChild(item);
                }
            });
        } else {
            resultsDiv.style.display = 'none';
        }
    }

    async function addMember(userId, userName) {
        if (addedUserIds.has(String(userId))) return;

        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', getCsrfToken());
        formData.append('compid', compId);
        formData.append('equipe_id', equipeId);
        formData.append('id_competidor', userId);

        const response = await fetch('/api/comp/add-member-to-team/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            addedUserIds.add(String(userId));
            const newItem = document.createElement('li');
            newItem.className = 'team-member-item';
            newItem.id = `member-item-${userId}`;
            newItem.innerHTML = `
                <span>${userName}</span>
                <button type="button" class="remove-member-btn" data-userid="${userId}">×</button>
            `;
            memberList.appendChild(newItem);
            handleSearch(searchInput.value);
        } else {
            alert('Erro ao adicionar membro.');
        }
    }

    async function removeMember(userId) {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', getCsrfToken());
        formData.append('compid', compId);
        formData.append('equipe_id', equipeId);
        formData.append('id_competidor', userId);

        const response = await fetch('/api/comp/remove-member-from-team/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            addedUserIds.delete(String(userId));
            document.getElementById(`member-item-${userId}`).remove();
        } else {
            alert('Erro ao remover membro.');
        }
    }

    searchInput.addEventListener('keyup', (e) => handleSearch(e.target.value.trim()));

    resultsDiv.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-member-btn')) {
            addMember(e.target.dataset.id, e.target.dataset.name);
        }
    });

    memberList.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-member-btn')) {
            if (confirm('Tem certeza que deseja remover este membro?')) {
                removeMember(e.target.dataset.userid);
            }
        }
    });
});