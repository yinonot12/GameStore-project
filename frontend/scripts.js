

async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post('http://localhost:5000/games', {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        });
        
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        getGames();
        
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

async function updateGame(gameId) {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.put(`http://localhost:5000/games/${gameId}`, {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        });

        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        getGames();
        
        alert('Game updated successfully!');
    } catch (error) {
        console.error('Error updating game:', error);
        alert('Failed to update game');
    }
}

async function deleteGame(gameId) {
    try {
        await axios.delete(`http://localhost:5000/games/${gameId}`);
        
        getGames();

        alert('Game deleted successfully!');
    } catch (error) {
        console.error('Error deleting game:', error);
        alert('Failed to delete game');
    }
}

async function getGames() {
    try {
        const response = await axios.get('http://localhost:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = '';

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: ${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                    <button onclick="updateGame(${game.id})">Update</button>
                    <button onclick="deleteGame(${game.id})">Delete</button>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to fetch games');
    }
}

async function adminLogin() {
    const username = document.getElementById('admin-username').value;
    const password = document.getElementById('admin-password').value;

    try {
        const response = await axios.post('http://localhost:5000/admin/login', {
            username: username,
            password: password
        });

        if (response.status === 200) {
            alert('Logged in successfully!');
            window.location.href = '/games.html';
        }
    } catch (error) {
        console.error('Error logging in:', error);
        alert('Login failed. Please check your credentials');
    }
}

async function adminLogout() {
    try {
        await axios.post('http://localhost:5000/admin/logout');
        alert('Logged out successfully!');
        window.location.href = '/login.html';
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Logout failed');
    }
}

async function loanGame() {
    const customerId = document.getElementById('customer-id').value;
    const gameId = document.getElementById('game-id').value;

    try {
        await axios.post('http://localhost:5000/loan', {
            customer_id: customerId,
            game_id: gameId
        });

        document.getElementById('customer-id').value = '';
        document.getElementById('game-id').value = '';

        alert('Game loaned successfully!');
    } catch (error) {
        console.error('Error loaning game:', error);
        alert('Failed to loan game');
    }
}

async function returnGame(loanId) {
    try {
        await axios.post(`http://localhost:5000/return_game/${loanId}`);
        
        alert('Game returned successfully!');
    } catch (error) {
        console.error('Error returning game:', error);
        alert('Failed to return game');
    }
}

async function getLoanedGames() {
    try {
        const response = await axios.get('http://localhost:5000/loaned_games');
        const loanedGamesList = document.getElementById('loaned-games-list');
        loanedGamesList.innerHTML = '';

        response.data.loans.forEach(loan => {
            loanedGamesList.innerHTML += `
                <div class="loan-card">
                    <p>Game: ${loan.game}</p>
                    <p>Customer: ${loan.customer}</p>
                    <p>Loan Date: ${loan.loan_date}</p>
                    <button onclick="returnGame(${loan.loan_id})">Return Game</button>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching loaned games:', error);
        alert('Failed to fetch loaned games');
    }
}

document.addEventListener('DOMContentLoaded', getGames);
