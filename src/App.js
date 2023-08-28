
import React, { useState } from 'react';

import LoginPage from './components/LoginPage';
import FlightList from './components/FlightsList';
import FlightByParams from './components/FlightByParams';
import CreateUserPage from './components/CreateUserPage';
import CreateCustomer from './components/CreateCustomer';

function App() {
  const [showLoginModal, setShowLoginModal] = useState(false);

  return (
    <div>

<button onClick={() => setShowLoginModal(true)}>Hi there, Please log in</button>

{/* Condition to render to LoginPage  */}
{showLoginModal && <LoginPage closeModal={() => setShowLoginModal(false)} />}
      <CreateUserPage/>
      <CreateCustomer/>
      <FlightByParams />

      <FlightList />

    </div>
  );
}

export default App;



