import React, { useState, useEffect } from 'react';

const ViewTicketsModal = () => {
    const [tickets, setTickets] = useState([]);
    const [showCancelConfirmation, setShowCancelConfirmation] = useState(false);
    const [selectedBookingCode, setSelectedBookingCode] = useState(null);

    useEffect(() => {
        fetchTickets();
    }, []);

    const fetchTickets = async () => {
        try {
            const userData = JSON.parse(localStorage.getItem('loggedInUser'));
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/buy', {
                headers: {
                    'UserID': userData.customer_id
                }
            });

            const ticketData = await response.json();
            setTickets(ticketData);
        } catch (error) {
            console.error('Error fetching tickets:', error);
        }
    };

    const handleCancelClick = (bookingCode) => {
        setSelectedBookingCode(bookingCode);
        setShowCancelConfirmation(true);
    };

    const confirmCancellation = async () => {
        try {
            const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/buy', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ booking_code: selectedBookingCode })
            });
    
            if (response.status === 200) {
                console.log(`Ticket ${selectedBookingCode} removed successfully.`);
                setTickets(prevTickets => prevTickets.filter(ticket => ticket.booking_code !== selectedBookingCode));
            } else {
                const data = await response.json();
                console.error(`Error removing ticket: ${data.error}`);
            }
        } catch (error) {
            console.error('Unexpected error while removing ticket:', error);
        } finally {
            setShowCancelConfirmation(false);
            setSelectedBookingCode(null);
        }
    };
    
    const declineCancellation = () => {
        setSelectedBookingCode(null);
        setShowCancelConfirmation(false);
    };

    return (
        <div className="modal">
            <div className="modal-header">
                <h2>My Tickets</h2>
            </div>
            <div className="modal-body">
                <table>
                    <thead>
                        <tr>
                            <th>Ticket Code</th>
                            <th>Flight ID</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tickets.map(ticket => (
                            <tr key={ticket.booking_code}>
                                <td>{ticket.booking_code}</td>
                                <td>{ticket.flight_id}</td>
                                <td>
                                    <button onClick={() => handleCancelClick(ticket.booking_code)}>Cancel</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                
                {showCancelConfirmation && (
                    <div className="cancel-ticket-modal">
                        Are you sure you want to cancel ticket with booking code: {selectedBookingCode}?
                        <button onClick={confirmCancellation}>Yes</button>
                        <button onClick={declineCancellation}>No</button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ViewTicketsModal;
