


import React, { useState, useEffect } from 'react';

const AirlineFlightsModal = () => {
    const [flights, setFlights] = useState([]);
    const [countries, setCountries] = useState([]);
    const [selectedFlight, setSelectedFlight] = useState(null);
    const [showAddFlightModal, setShowAddFlightModal] = useState(false);
    const [newFlightData, setNewFlightData] = useState({
        departure_date: '',
        departure_time: '',
        landing_date: '',
        landing_time: '',
        origin_country_id: '',
        destination_country_id: '',
        remaining_tickets: ''
    });

    useEffect(() => {
        fetchCountries();
        fetchFlights();
    }, []);

    const fetchCountries = async () => {
        try {
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/country');
            const countryData = await response.json();
            setCountries(countryData);
        } catch (error) {
            console.error('Error fetching countries:', error);
        }
    };

    const fetchFlights = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/flights/airline', {
                method: 'GET',
                headers: {
                    'UserRole': userData.role,
                    'UserID': userData.air_line_company_id,
                    'Content-Type': 'application/json'
                },
            });

            const flightData = await response.json();
            setFlights(flightData);
        } catch (error) {
            console.error('Error fetching flights:', error);
        }
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewFlightData(prevData => ({ ...prevData, [name]: value }));
    };

    const handleAddFlight = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            
            const departure = `${newFlightData.departure_date} ${newFlightData.departure_time}`;
            const landing = `${newFlightData.landing_date} ${newFlightData.landing_time}`;
            const payload = {
                origin_country_id: Number(newFlightData.origin_country_id),
                destination_country_id: Number(newFlightData.destination_country_id),
                departure_time: departure,
                landing_time: landing,
                remaining_tickets: newFlightData.remaining_tickets
            };

            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/flights', {
                method: 'POST',
                headers: {
                    'UserRole': userData.role,
                    'UserID': userData.air_line_company_id,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                setShowAddFlightModal(false);
                fetchFlights();
            } else {
                console.error('Error adding flight:', await response.json());
            }
        } catch (error) {
            console.error('Error adding flight:', error);
        }
    };

    return (
        <div className="modal">
            <div className="modal-header">
                <h2>My Flights</h2>
                <button onClick={() => setShowAddFlightModal(true)}>Add Flight</button>
            </div>

            {showAddFlightModal && (
                <div className="add-flight-modal">
                    <h3>Add New Flight</h3>
                    <input type="date" name="departure_date" onChange={handleInputChange} value={newFlightData.departure_date} />
                    <input type="time" name="departure_time" onChange={handleInputChange} value={newFlightData.departure_time} />
                    <input type="date" name="landing_date" onChange={handleInputChange} value={newFlightData.landing_date} />
                    <input type="time" name="landing_time" onChange={handleInputChange} value={newFlightData.landing_time} />
                    <label>
                        Origin Country:
                        <select name="origin_country_id" onChange={handleInputChange} value={newFlightData.origin_country_id}>
                            <option value="">Select Country</option>
                            {countries.map(country => (
                                <option key={country.id} value={country.id}>
                                    {country.country_name}
                                </option>
                            ))}
                        </select>
                    </label>
                    <label>
                        Destination Country:
                        <select name="destination_country_id" onChange={handleInputChange} value={newFlightData.destination_country_id}>
                            <option value="">Select Country</option>
                            {countries.map(country => (
                                <option key={country.id} value={country.id}>
                                    {country.country_name}
                                </option>
                            ))}
                        </select>
                    </label>
                    <input type="number" name="remaining_tickets" placeholder="Remaining Tickets" onChange={handleInputChange} value={newFlightData.remaining_tickets} />
                    <button onClick={handleAddFlight}>Submit</button>
                    <button onClick={() => setShowAddFlightModal(false)}>Cancel</button>
                </div>
            )}

            <div className="modal-body">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Airline Company</th>
                            <th>Origin</th>
                            <th>Destination</th>
                            <th>Departure Time</th>
                            <th>Landing Time</th>
                            <th>Remaining Tickets</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {flights.map(flight => (
                            <tr key={flight.id}>
                                <td>{flight.id}</td>
                                <td>{flight.airline_company.name}</td>
                                <td>{flight.origin_country.name}</td>
                                <td>{flight.destination_country.name}</td>
                                <td>{flight.departure_time}</td>
                                <td>{flight.landing_time}</td>
                                <td>{flight.remaining_tickets}</td>
                                <td><button onClick={() => setSelectedFlight(flight)}>Details</button></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AirlineFlightsModal;
