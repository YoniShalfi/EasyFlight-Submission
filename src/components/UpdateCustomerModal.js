
import React, { useState, useEffect } from 'react';

const UpdateCustomerModal = ({ isOpen, closeModal, updateCustomer }) => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    address: '',
    phone_no: '',
    credit_card_no: '',
  });

  const [changedData, setChangedData] = useState({});

  const [username, setUsername] = useState('');

  useEffect(() => {
    const storedUsername = localStorage.getItem('name');
    setUsername(storedUsername);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    setChangedData((prevChangedData) => ({ ...prevChangedData, [name]: value }));
  };

  const handleSubmit = async () => {
    try {
      const userData = JSON.parse(localStorage.getItem('loggedInUser'));
      const response = await fetch('https://prod-easyflight-backend.azurewebsites.net/customers', {
        method: 'PUT',
        headers: {
          'name': userData.name,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(changedData),
      });

      if (response.ok) {
        const updatedData = await response.json();
        updateCustomer(updatedData);
        closeModal();
      } else {
        console.error('Error updating customer');
      }
    } catch (error) {
      console.error('Error updating customer:', error);
    }
  };


  
  return (
    <div className={`modal ${isOpen ? 'open' : 'closed'}`}>
      <div className="modal-header">
        <h2>Update Customer Data</h2>
      </div>
      <div className="modal-body">
        <form>
          <label>
            First Name:
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
            />
          </label>
          <label>
            Last Name:
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
            />
          </label>
          <label>
            Address:
            <input
              type="text"
              name="address"
              value={formData.address}
              onChange={handleChange}
            />
          </label>
          <label>
            Phone Number:
            <input
              type="text"
              name="phone_no"
              value={formData.phone_no}
              onChange={handleChange}
            />
          </label>
          <label>
            Credit Card Number:
            <input
              type="text"
              name="credit_card_no"
              value={formData.credit_card_no}
              onChange={handleChange}
            />
          </label>
          <button type="button" onClick={handleSubmit}>
            Update
          </button>
          <button type="button" onClick={closeModal}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
};

export default UpdateCustomerModal;



