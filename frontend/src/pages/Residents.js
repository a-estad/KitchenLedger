import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Residents = () => {
  const [residents, setResidents] = useState([]);

  useEffect(() => {
    // Fetch residents data from the Django API
    axios.get('http://127.0.0.1:8000/api/residents/')  // Update this URL based on your API
      .then(response => {
        setResidents(response.data);
      })
      .catch(error => {
        console.error('Error fetching residents:', error);
      });
  }, []);

  return (
    <div>
      <h1>Residents</h1>
      <ul>
        {residents.map(resident => (
          <li key={resident.id}>
            {resident.name} (Room: {resident.room_number}) - Balance: ${resident.balance}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Residents;
