

import React, { useState, useEffect } from 'react';

import LoginPage from './components/LoginPage';
import FlightList from './components/FlightsList';
import FlightByParams from './components/FlightByParams';
import CreateUserPage from './components/CreateUserPage';
import CreateCustomer from './components/CreateCustomer';
import AdminCustomersModal from './components/AdminCustomersModal'; 
import AdminAirlineModal from './components/AdminAirlineModal';
import AirlineFlightsModal from './components/AirlineFlightsModal'; 
import BuyTicketModal from './components/BuyTicketModal';
import ViewTicketsModal from './components/ViewTicketsModal';
import RefreshButton from './components/Refresh';
import mainPic from './mainPic.jpg';
import UpdateCustomerModal from './components/UpdateCustomerModal';


function App() {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showCustomersModal, setShowCustomersModal] = useState(false);
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [showFlightsModal, setShowFlightsModal] = useState(false); 
  const [showAirlineModal, setshowAirlineModal] = useState(false);
  const [showViewTicketsModal, setShowViewTicketsModal] = useState(false);
  const [selectedBookingCode, setSelectedBookingCode] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('loggedInUser');
    if (storedUser) {
      setLoggedInUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <div>
      <img src={mainPic} alt="mainPic" width="30%" height="30%" />
      <RefreshButton />
      <button onClick={() => setShowLoginModal(true)}>Hi there, Please log in</button>

      {showLoginModal && <LoginPage closeModal={() => setShowLoginModal(false)} />}

      {loggedInUser && loggedInUser.role === 'Administrator' &&
        <button onClick={() => setShowCustomersModal(true)}>See All Customers</button>
      }

      {loggedInUser && loggedInUser.role === 'Administrator' &&
        <button onClick={() => setshowAirlineModal(true)}>See All Air Lines</button>
      }

      {loggedInUser && loggedInUser.role === 'Air Line Company' && 
        <button onClick={() => setShowFlightsModal(true)}>See My Flights</button>
      }

      {showCustomersModal && <AdminCustomersModal />}
      {showAirlineModal && <AdminAirlineModal />}
      {showFlightsModal && <AirlineFlightsModal />}

      {!loggedInUser && (
        <>
          <CreateUserPage/>
          <CreateCustomer/>
        </>
      )}

      <FlightByParams />
      <br></br>
      <br></br>
      
      <FlightList />
      <br></br>
      <br></br>
      <UpdateCustomerModal />
      <br></br>
      <br></br>
      {loggedInUser && loggedInUser.role === 'User' && 
        <>
          <button onClick={() => setShowViewTicketsModal(true)}>View My Tickets</button>
          <BuyTicketModal />
          {showViewTicketsModal && 
            <ViewTicketsModal 
              onClose={() => setShowViewTicketsModal(false)} 
              onSelectTicketToCancel={(bookingCode) => {
                setSelectedBookingCode(bookingCode);
              }}
            />
          }
        </>
      }
    </div>
  );
}

export default App;
