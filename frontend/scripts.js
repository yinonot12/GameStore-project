document.addEventListener("DOMContentLoaded", () => {
    loadGames();
    loadLoanedGames();
});

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.success) {
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            // Load initial data
            loadGames();
            loadLoanedGames();
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please check your credentials and try again.');
    }
}

async function loadGames() {
    const response = await fetch("http://127.0.0.1:5501/games", {
        method: "GET",
        credentials: "include"
    });
    
    const gamesList = document.getElementById("games-list");
    gamesList.innerHTML = "";

    if (response.ok) {
        const games = await response.json();
        games.forEach(game => {
            const li = document.createElement("li");
            li.textContent = `${game.title} - ${game.genre} - $${game.price} - Available: ${game.quantity}`;
            
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.onclick = () => deleteGame(game.id);
            li.appendChild(deleteButton);
            
            gamesList.appendChild(li);
        });
    } else {
        console.error("Failed to load games.");
    }
}

async function addGame() {
    const title = document.getElementById("game-title").value;
    const genre = document.getElementById("game-genre").value;
    const price = document.getElementById("game-price").value;
    const quantity = document.getElementById("game-quantity").value;
    
    const response = await fetch("http://127.0.0.1:5501/games", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, genre, price, quantity })
    });
    
    if (response.ok) {
        loadGames();
    } else {
        console.error("Failed to add game.");
    }
}

async function deleteGame(gameId) {
    const response = await fetch(`http://127.0.0.1:5501/games/${gameId}`, {
        method: "DELETE",
        credentials: "include"
    });
    
    if (response.ok) {
        loadGames();
    } else {
        console.error("Failed to delete game.");
    }
}

async function loadLoanedGames() {
    const response = await fetch("http://127.0.0.1:5501/loans", {
        method: "GET",
        credentials: "include"
    });
    
    const loanedGamesList = document.getElementById("loaned-games-list");
    loanedGamesList.innerHTML = "";

    if (response.ok) {
        const loans = await response.json();
        loans.forEach(loan => {
            const li = document.createElement("li");
            li.textContent = `${loan.title} loaned to ${loan.customer}`;
            loanedGamesList.appendChild(li);
        });
    } else {
        console.error("Failed to load loaned games.");
    }
}

async function loanGame() {
    const gameId = document.getElementById("loan-game-id").value;
    const customerId = document.getElementById("loan-customer-id").value;
    
    const response = await fetch("http://127.0.0.1:5501/loans", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, customer_id: customerId })
    });
    
    if (response.ok) {
        loadLoanedGames();
    } else {
        console.error("Failed to loan game.");
    }
}

async function logout() {
    await fetch("http://127.0.0.1:5501/logout", {
        method: "POST",
        credentials: "include"
    });
    document.getElementById("login-container").style.display = "block";
    document.getElementById("dashboard").style.display = "none";
}
