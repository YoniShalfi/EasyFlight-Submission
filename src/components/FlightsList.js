import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Modal from './Modal';
import './FlightList.css';

function FlightList() {
  const [flights, setFlights] = useState([]);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);  
  const [transitionState, setTransitionState] = useState('entering');  

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('https://easyflight-prod.azurewebsites.net/flights');
        setFlights(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const fetchFlightDetails = async (flightId) => {
    try {
      const response = await axios.get(`https://easyflight-prod.azurewebsites.net/flights/${flightId}`);
      setSelectedFlight(response.data);
      setShowModal(true);
    } catch (error) {
      console.error('Error fetching flight details:', error);
    }
  };

  const gotoNextFlight = () => {
    setTransitionState('exiting');
    setTimeout(() => {
      setCurrentPage((prev) => Math.min(prev + 1, flights.length - 1));
      setTransitionState('entering');
    }, 300);
  };

  const gotoPreviousFlight = () => {
    setTransitionState('exiting');
    setTimeout(() => {
      setCurrentPage((prev) => Math.max(prev - 1, 0));
      setTransitionState('entering');
    }, 300);
  };

  const currentFlight = flights[currentPage] || {};

  return (
    <div>
      <h1>Flight List</h1>

      <div className={`flight-detail ${transitionState}`}>
        <strong>Flight from </strong> {currentFlight.origin_country?.name}<br />
        <strong>to</strong> {currentFlight.destination_country?.name}<br />
        <strong>With</strong> {currentFlight.airline_company?.name}<br />
        <strong>Departure Time:</strong> {currentFlight.departure_time}<br />
        <strong>Landing Time:</strong> {currentFlight.landing_time}<br />
        <strong>For more Details {'->'}</strong>
        <button onClick={() => fetchFlightDetails(currentFlight.id)}>{"click here"}</button><br />
      </div>

      <button onClick={gotoPreviousFlight} disabled={currentPage === 0}>Previous</button>
      <button onClick={gotoNextFlight} disabled={currentPage === flights.length - 1}>Next</button>

      <Modal show={showModal} onClose={() => setShowModal(false)}>
        {selectedFlight && (
          <div>
            <h2>Flight Details</h2>
            <strong>Flight ID:</strong> {selectedFlight.id}<br />
            <strong>Airline:</strong> {selectedFlight.airline_company.name}<br />
            <strong>Origin Country:</strong> {selectedFlight.origin_country.name}<br />
            <strong>Destination Country:</strong> {selectedFlight.destination_country.name}<br />
            <strong>Departure Time:</strong> {selectedFlight.departure_time}<br />
            <strong>Landing Time:</strong> {selectedFlight.landing_time}<br />
            <strong>Remaining Tickets:</strong> {selectedFlight.remaining_Tickets}<br />
          </div>
        )}
      </Modal>
    </div>
  );
}

export default FlightList;



