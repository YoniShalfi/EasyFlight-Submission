import React, { useState, useEffect } from 'react';

const BuyTicketModal = () => {
    const [flights, setFlights] = useState([]);
    const [selectedFlight, setSelectedFlight] = useState(null);
    const [ticketData, setTicketData] = useState({
        flight_id: '',
        tickets_number: 1,
        credit_card: ''
    });

    useEffect(() => {
        fetchFlights();
    }, []);

    const fetchFlights = async () => {
        try {
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/flights');
            const flightData = await response.json();
            setFlights(flightData);
        } catch (error) {
            console.error('Error fetching flights:', error);
        }
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setTicketData(prevData => ({ ...prevData, [name]: value }));
    };

    const handlePurchase = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/buy', {
                method: 'POST',
                headers: {
                    'UserID': userData.customer_id,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ticketData)
            });

            if (response.ok) {
                const responseData = await response.json();
                console.log('Ticket purchase successful:', responseData);
            } else {
                console.error('Error purchasing ticket:', await response.json());
            }
        } catch (error) {
            console.error('Error purchasing ticket:', error);
        }
    };

    return (
        <div className="modal">
            <div className="modal-header">
                <h2>Buy Tickets</h2>
            </div>
            <div className="modal-body">
            <label>
                    Select Flight:
                    <select name="flight_id" onChange={handleInputChange} value={ticketData.flight_id}>
                        <option value="">Select Flight</option>
                        {flights.map(flight => (
                            <option key={flight.id} value={flight.id}>
                               flight id: {flight.id} - {flight.origin_country.name} to {flight.destination_country.name}
                            </option>
                        ))}
                    </select>
                </label>
                <label>
                    Number of Tickets:
                    <input type="number" name="tickets_number" min="1" onChange={handleInputChange} value={ticketData.tickets_number} />
                </label>
                <label>
                    Credit Card:
                    <input type="text" name="credit_card" placeholder="Credit Card Number" onChange={handleInputChange} value={ticketData.credit_card} />
                </label>
                <button onClick={handlePurchase}>Purchase</button>
            </div>
        </div>
    );
}

export default BuyTicketModal;
