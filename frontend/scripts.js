const API_BASE_URL = 'http://localhost:5501';

const fetchConfig = {
    headers: {
        'Content-Type': 'application/json'
    }
};

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('isLoggedIn') === 'true') {
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        loadGames();
    
    }
});

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            ...fetchConfig,
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            await loadGames();
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

async function loadGames() {
    try {
        const response = await fetch(`${API_BASE_URL}/games`, {
            method: 'GET',
            ...fetchConfig
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const games = await response.json();
        displayGames(games);
    } catch (error) {
        console.error('Error loading games:', error);
    }
}

function displayGames(games) {
    const gamesContainer = document.getElementById('games-container');
    gamesContainer.innerHTML = '';

    games.forEach(game => {
        const gameCard = document.createElement('div');
        gameCard.className = 'game-card';
        gameCard.innerHTML = `
            <h3>${game.title}</h3>
            <p><strong>Genre:</strong> ${game.genre}</p>
            <p><strong>Price:</strong> $${game.price.toFixed(2)}</p>
            <p><strong>Quantity:</strong> ${game.quantity}</p>
            <div class="game-actions">
                <button onclick="editGame(${game.id})" class="btn-edit">Edit</button>
                <button onclick="deleteGame(${game.id})" class="btn-delete">Delete</button>
            </div>
        `;
        gamesContainer.appendChild(gameCard);
    });
}

async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    if (!title || !genre || !price || !quantity) {
        alert('Please fill in all fields');
        return;
    }

    const gameData = {
        title,
        genre,
        price: parseFloat(price),
        quantity: parseInt(quantity)
    };

    console.log('Sending game data:', gameData);  // Debug log

    try {
        const response = await fetch(`${API_BASE_URL}/games`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(gameData)
        });

        console.log('Response status:', response.status);  // Debug log
        const data = await response.json();
        console.log('Response data:', data);  // Debug log

        if (response.ok && data.success) {
            alert('Game added successfully!');
            document.getElementById('game-title').value = '';
            document.getElementById('game-genre').value = '';
            document.getElementById('game-price').value = '';
            document.getElementById('game-quantity').value = '';
            await loadGames();
        } else {
            throw new Error(data.error || 'Failed to add game');
        }
    } catch (error) {
        console.error('Error adding game:', error);
        alert(error.message || 'Failed to add game');
    }
}

async function deleteGame(gameId) {
    if (!confirm('Are you sure you want to delete this game?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/games/${gameId}`, {
            method: 'DELETE',
            ...fetchConfig
        });

        const data = await response.json();

        if (data.success) {
            alert('Game deleted successfully!');
            await loadGames();
        } else {
            throw new Error(data.message || 'Failed to delete game');
        }
    } catch (error) {
        console.error('Error deleting game:', error);
        alert(error.message || 'Failed to delete game');
    }
}

async function editGame(gameId) {
    try {
        const response = await fetch(`${API_BASE_URL}/games/${gameId}`, {
            method: 'GET',
            ...fetchConfig
        });

        if (!response.ok) {
            throw new Error('Failed to fetch game details');
        }

        const game = await response.json();
        
        const gamesContainer = document.getElementById('games-container');
        gamesContainer.innerHTML = `
            <div class="edit-form">
                <h3>Edit Game</h3>
                <div class="form-group">
                    <label for="edit-title">Title</label>
                    <input type="text" id="edit-title" value="${game.title}" required>
                </div>
                <div class="form-group">
                    <label for="edit-genre">Genre</label>
                    <input type="text" id="edit-genre" value="${game.genre}" required>
                </div>
                <div class="form-group">
                    <label for="edit-price">Price</label>
                    <input type="number" id="edit-price" value="${game.price}" step="0.01" required>
                </div>
                <div class="form-group">
                    <label for="edit-quantity">Quantity</label>
                    <input type="number" id="edit-quantity" value="${game.quantity}" required>
                </div>
                <div class="edit-actions">
                    <button onclick="saveGameEdit(${gameId})" class="btn-save">Save</button>
                    <button onclick="loadGames()" class="btn-cancel">Cancel</button>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading game for edit:', error);
        alert('Failed to load game for editing');
    }
}

async function saveGameEdit(gameId) {
    try {
        const title = document.getElementById('edit-title').value;
        const genre = document.getElementById('edit-genre').value;
        const price = document.getElementById('edit-price').value;
        const quantity = document.getElementById('edit-quantity').value;

        if (!title || !genre || !price || !quantity) {
            alert('Please fill in all fields');
            return;
        }

        const response = await fetch(`${API_BASE_URL}/games/${gameId}`, {
            method: 'PUT',
            ...fetchConfig,
            body: JSON.stringify({
                title,
                genre,
                price: parseFloat(price),
                quantity: parseInt(quantity)
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('Game updated successfully!');
            await loadGames();
        } else {
            throw new Error(data.message || 'Failed to update game');
        }
    } catch (error) {
        console.error('Error updating game:', error);
        alert(error.message || 'Failed to update game');
    }
}

function logout() {
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}



// Initialize when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Scripts loaded successfully');
});

async function fetchGame(gameId) {
    const response = await fetch(`${API_BASE_URL}/games/${gameId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return response.json();
}

