import React, { useState } from 'react';

const CreateUserPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [userRole, setUserRole] = useState(2); // default to user role

    const handleCreateUser = async () => {
        try {
            const response = await fetch('https://easyflight-prod.azurewebsites.net/createUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    password,
                    email,
                    user_role_id: userRole,
                }),
            });
            if (response.ok) {
                console.log('User created successfully!');
            } else {
                console.error('Failed to create user.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h2>Create User</h2>
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
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <button onClick={handleCreateUser}>Create User</button>
        </div>
    );
};

export default CreateUserPage;
