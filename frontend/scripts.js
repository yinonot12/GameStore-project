// Function to fetch all games
async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: $${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

// Function to add a new game to the database
async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        });

        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        // Refresh the games list
        getGames();

        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

// Function to login as admin
async function adminLogin() {
    const username = document.getElementById('admin-username').value;
    const password = document.getElementById('admin-password').value;
    
    try {
        const response = await axios.post('http://127.0.0.1:5000/admin/login', {
            username: username,
            password: password
        });
        alert(response.data.message);

        // After successful login, hide the login form and display the admin panel
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('admin-panel').style.display = 'block';

        // Fetch the list of games
        getGames();
    } catch (error) {
        console.error('Error logging in:', error);
        alert('Login failed. Please check your credentials.');
    }
}

// Function to logout from the admin panel
async function adminLogout() {
    try {
        const response = await axios.post('http://127.0.0.1:5000/admin/logout');
        alert(response.data.message);

        // Return to the login form and hide the admin panel
        document.getElementById('login-container').style.display = 'block';
        document.getElementById('admin-panel').style.display = 'none';
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Logout failed.');
    }
}

// Load all games when the page loads
document.addEventListener('DOMContentLoaded', getGames);
