import React, { useState } from 'react';

const CreateCustomer = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [address, setAddress] = useState('');
    const [phoneNo, setPhoneNo] = useState('');
    const [creditCardNum, setCreditCardNum] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    const handleAddCustomer = async () => {
        try {
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/customers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    address,
                    phone_no: phoneNo,
                    credit_card_num: creditCardNum,
                    username,
                    password,
                    email,
                }),
            });
            if (response.ok) {
                console.log('Customer added successfully!');
            } else {
                console.error('Failed to add customer.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h2>Add Customer</h2>
            <input
                type="text"
                placeholder="First Name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
            />
            <input
                type="text"
                placeholder="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
            />

            <input
                type="text"
                placeholder="address"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
            />

            <input
                type="tel"
                placeholder="phone number"
                value={phoneNo}
                onChange={(e) => setPhoneNo(e.target.value)}
                pattern="^05\d{8}$"
                title="Please enter a valid Israeli mobile phone number without the country code."
            />

            <input
            type="text"
            placeholder="Credit Card Number"
            value={creditCardNum}
            onChange={(e) => setCreditCardNum(e.target.value)}
            pattern="^\d{4}-\d{4}-\d{4}-\d{4}$"
            title="Please enter a valid credit card number in the format XXXX-XXXX-XXXX-XXXX."
            />


            <input
                type="password"
                placeholder="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                type="text"
                placeholder="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <input
                type="text"
                placeholder="email"
                value={email}
                pattern="^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"
                title="Please enter a valid email address."
                onChange={(e) => setEmail(e.target.value)}
            />

            




            
            <button onClick={handleAddCustomer}>Add Customer</button>
        </div>
    );
};

export default CreateCustomer;
