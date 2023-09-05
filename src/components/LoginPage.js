
import React, { useState, useEffect } from 'react';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loggedInUser, setLoggedInUser] = useState(null); 

    // Load user data from local storage  
    useEffect(() => {
        const savedUser = localStorage.getItem('loggedInUser');
        if (savedUser && savedUser !== 'undefined') {
            setLoggedInUser(JSON.parse(savedUser));
        }
    }, []);
    
    const handleLogin = async () => {
        try {
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                // credentials: 'include',
                body: JSON.stringify({ username, password }),
            });
    
            const [userData, status] = await response.json(); 
    
            if (status === 200) {
                setLoggedInUser(userData); // Store the user data
                // Save user data to localStorage
                localStorage.setItem('loggedInUser', JSON.stringify(userData));
            } else {
                console.error('Login failed');
            }
    
            console.log('Login response:', userData); // Log the user data
        } catch (error) {
            console.error('Error during login:', error);
        }
    };
    
    const handleLogout = async () => {
        // try {
            console.log('body',{ id: loggedInUser.id, login_token: loggedInUser })
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // credentials: 'include',
                body: JSON.stringify({ id: loggedInUser.id, login_token: loggedInUser }),
            });

            if (response.status === 200 || response.status === 410) {
                localStorage.removeItem('loggedInUser');
                setLoggedInUser(null);
            } else {
                console.error('Logout failed');
            }
       // } catch (error) {
       //     console.error('Error during logout:', error);
       //}
    };

    return (
        <div>
            {loggedInUser ? (
                <div>
                    <p>You are logged in as {loggedInUser.name}</p>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <div>
                    <p>Please log in:</p>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button onClick={handleLogin}>Login</button>
                </div>
            )}
        </div>
    );
};

export default LoginPage;


