
import React, { useState, useEffect } from 'react';

const AdminCustomersModal = () => {
    const [customers, setCustomers] = useState([]);
    const [selectedCustomer, setSelectedCustomer] = useState(null);

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/customers', {
                method: 'GET',
                headers: {
                    'UserRole': userData.role,
                    'Content-Type': 'application/json'
                },
            });

            const customersData = await response.json();
            setCustomers(customersData);
        } catch (error) {
            console.error('Error fetching customers:', error);
        }
    };

    const getCustomerById = async (id) => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch(`https://prod-easyflight-backend.azurewebsites.net/customers/${id}`, {
                method: 'GET',
                headers: {
                    'UserRole': userData.role,
                    'Content-Type': 'application/json'
                },
            });

            const customerData = await response.json();
            setSelectedCustomer(customerData);
        } catch (error) {
            console.error(`Error fetching customer by ID: ${id}`, error);
        }
    };

    const deleteCustomer = async (customerId) => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch(`https://prod-easyflight-backend.azurewebsites.net/customers/${customerId}`, {
                method: 'DELETE',
                headers: {
                    'UserRole': userData.role
                }
            });
    
            if (response.ok && response.headers.get('content-length')) {
                const result = await response.json();
                if (result.success) {
                    alert('Customer deleted successfully');
                    // Refresh the customer list
                    fetchCustomers();
                    setSelectedCustomer(null);
                } else {
                    alert(result.error);
                }
            } else {
                console.error('Server responded with:', response.status, response.statusText);
            }
        } catch (error) {
            console.error('Error during customer deletion:', error);
        }
    };
    

    return (
        <div className="modal">
            {/* Header */}
            <div className="modal-header">
                <h2>All Customers</h2>
            </div>

            {/* Body */}
            <div className="modal-body">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {customers.map(customer => (
                            <tr key={customer.id}>
                                <td>{customer.id}</td>
                                <td>{customer.first_name}</td>
                                <td>{customer.last_name}</td>
                                <td>
                                    <button onClick={() => getCustomerById(customer.id)}>Details</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                
                {/* Selected Customer Details */}
                {selectedCustomer && (
                    <div className="customer-details">
                        <h3>Details for {selectedCustomer.first_name} {selectedCustomer.last_name}</h3>
                        <p><strong>Address:</strong> {selectedCustomer.address}</p>
                        <p><strong>Phone:</strong> {selectedCustomer.phone_no}</p>
                        <p><strong>Credit Card:</strong> {selectedCustomer.credit_card_no}</p>
                        <button onClick={() => deleteCustomer(selectedCustomer.id)}>Delete Customer</button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdminCustomersModal;
