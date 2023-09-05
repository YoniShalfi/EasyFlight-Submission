
import React, { useState, useEffect } from 'react';

const AdminAirlineModal = () => {
    const [airlines, setAirlines] = useState([]);
    const [selectedAirline, setSelectedAirline] = useState(null);
    const [airlineForm, setAirlineForm] = useState({ name: '', country_id: null });
    const [countries, setCountries] = useState([]);

    useEffect(() => {
        fetchAirlines();
        fetchCountries();
    }, []);

    const fetchAirlines = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/airline', {
                method: 'GET',
                headers: {
                    'UserRole': userData.role,
                    'Content-Type': 'application/json'
                },
            });
            const airlineData = await response.json();
            setAirlines(airlineData);
        } catch (error) {
            console.error('Error fetching airlines:', error);
        }
    };

    const fetchCountries = async () => {
        try {
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/country');
            const countryData = await response.json();
            setCountries(countryData);
        } catch (error) {
            console.error('Error fetching countries:', error);
        }
    };

    const getAirlineById = async (id) => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch(`https://prod-easyflight-backend.azurewebsites.net/${id}`, {
                method: 'GET',
                headers: {
                    'UserRole': userData.role,
                    'Content-Type': 'application/json'
                },
            });
            const airlineData = await response.json();
            setSelectedAirline(airlineData);
        } catch (error) {
            console.error(`Error fetching airline by ID: ${id}`, error);
        }
    };

    const deleteAirline = async (airlineId) => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch(`https://prod-easyflight-backend.azurewebsites.net/${airlineId}`, {
                method: 'DELETE',
                headers: {
                    'UserRole': userData.role
                }
            });
        } catch (error) {
            console.error('Error during airline deletion:', error);
        }
    };

    const addAirline = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/airline', {
                method: 'POST',
                headers: {
                    'UserRole': userData.role,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(airlineForm)
            });
            if (response.ok) {
                alert('Airline added successfully');
                fetchAirlines();
            } else {
                const error = await response.json();
                alert(error.error);
            }
        } catch (error) {
            console.error('Error adding airline:', error);
        }
    };

    return (
        <div className="modal">
            {/* Header */}
            <div className="modal-header">
                <h2>Air Lines</h2>
            </div>

            {/* Body */}
            <div className="modal-body">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {airlines.map(airline => (
                            <tr key={airline.id}>
                                <td>{airline.id}</td>
                                <td>{airline.air_line_name}</td>
                                <td>
                                    <button onClick={() => getAirlineById(airline.id)}>Details</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Selected Airline Details */}
                {selectedAirline && (
                    <div className="airline-details">
                        <h3>Details for {selectedAirline.air_line_name} </h3>
                        <button onClick={() => deleteAirline(selectedAirline.id)}>Delete airline</button>
                    </div>
                )}

                {/* Form to Add New Airline */}
                <div className="add-airline-form">
                    <h3>Add New Airline</h3>
                    <label>
                        Airline Name:
                        <input 
                            type="text" 
                            value={airlineForm.name} 
                            onChange={e => setAirlineForm(prev => ({ ...prev, name: e.target.value }))} 
                        />
                    </label>
                    <label>
                        Country:
                        <select 
                            value={airlineForm.country_id || ''} 
                            onChange={e => setAirlineForm(prev => ({ ...prev, country_id: Number(e.target.value) }))}
                        >
                            <option value="" disabled>Select Country</option>
                            {countries.map(country => (
                                <option key={country.id} value={country.id}>{country.country_name}</option>
                            ))}
                        </select>
                    </label>
                    <button onClick={addAirline}>Add Airline</button>
                </div>
            </div>
        </div>
    );
}

export default AdminAirlineModal;
