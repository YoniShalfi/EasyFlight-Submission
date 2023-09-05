import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Modal from './Modal';
import './FlightByParams.css';

function FlightByParams() {
  const [originCountry, setOriginCountry] = useState('');
  const [destinationCountry, setDestinationCountry] = useState('');
  const [airlineCompany, setAirlineCompany] = useState('');
  const [flights, setFlights] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [transitionState, setTransitionState] = useState('entering');
  const [selectedFlight, setSelectedFlight] = useState(null);  
  const [showModal, setShowModal] = useState(false);  
  const [countries, setCountries] = useState([]);
  const [airlines, setAirlines] = useState([]);

  useEffect(() => {
    const fetchCountriesAndAirlines = async () => {
      try {
        const countriesResponse = await axios.get('https://prod-easyflight-backend.azurewebsites.net//country');
        setCountries(countriesResponse.data);

        const airlinesResponse = await axios.get('https://prod-easyflight-backend.azurewebsites.net//airline');
        setAirlines(airlinesResponse.data);
      } catch (error) {
        console.error('Error fetching countries or airlines:', error);
      }
    };

    fetchCountriesAndAirlines();
  }, []);

  const fetchFlightsByParams = async () => {
    try {
      let params = {};

      if (originCountry) {
        params.origin_country__name = originCountry;
      }
      if (destinationCountry) {
        params.destination_country__name = destinationCountry;
      }
      if (airlineCompany) {
        params.airline_company__name = airlineCompany;
      }

      const response = await axios.get('https://prod-easyflight-backend.azurewebsites.net//flights/parameters', { params });
      setFlights(response.data);
    } catch (error) {
      console.error('Error fetching flights by parameters:', error);
    }
  };

  const fetchFlightDetails = async (flightId) => {
    try {
      const response = await axios.get(`https://prod-easyflight-backend.azurewebsites.net//flights/${flightId}`);
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
      <h1>Search Flights</h1>
      
      <div>
        <label>
          Origin Country:
          <select value={originCountry} onChange={e => setOriginCountry(e.target.value)}>
            <option value="">Select a Country</option>
            {countries.map(country => <option key={country.id} value={country.country_name}>{country.country_name}</option>)}
          </select>
        </label>
      </div>
      
      <div>
        <label>
          Destination Country:
          <select value={destinationCountry} onChange={e => setDestinationCountry(e.target.value)}>
            <option value="">Select a Country</option>
            {countries.map(country => <option key={country.id} value={country.country_name}>{country.country_name}</option>)}
          </select>
        </label>
      </div>
      
      <div>
        <label>
          Airline Company:
          <select value={airlineCompany} onChange={e => setAirlineCompany(e.target.value)}>
            <option value="">Select an Airline</option>
            {airlines.map(airline => <option key={airline.id} value={airline.air_line_name}>{airline.air_line_name}</option>)}
          </select>
        </label>
      </div>

      <button onClick={fetchFlightsByParams}>Search</button>

      {flights.length > 0 && (
        <>
          <h2>Flights</h2>
          
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
        </>
      )}

      <Modal show={showModal} onClose={() => setShowModal(false)}>
        {selectedFlight && (
          <div>
            <h2>Flight Details</h2>
            <strong>Flight ID:</strong> {selectedFlight.id}<br />
            <strong>Airline:</strong> {selectedFlight.airline_company?.name}<br />
            <strong>Origin Country:</strong> {selectedFlight.origin_country?.name}<br />
            <strong>Destination Country:</strong> {selectedFlight.destination_country?.name}<br />
            <strong>Departure Time:</strong> {selectedFlight.departure_time}<br />
            <strong>Landing Time:</strong> {selectedFlight.landing_time}<br />
          </div>
        )}
      </Modal>
    </div>
  );
}

export default FlightByParams;

