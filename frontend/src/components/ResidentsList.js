import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResidentsList = () => {
  const [residents, setResidents] = useState([]);

  useEffect(() => {
    axios.get('/api/residents/')
      .then(response => {
        setResidents(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the residents!', error);
      });
  }, []);

  return (
    <div>
      <h1>Residents</h1>
      <ul>
        {residents.map(resident => (
          <li key={resident.id}>
            {resident.name} (Room: {resident.room_number})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ResidentsList;
