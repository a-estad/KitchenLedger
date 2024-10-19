import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TestAPI = () => {
  const [residents, setResidents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch data from the Django API
    axios.get('http://127.0.0.1:8000/api/residents/')
      .then(response => {
        setResidents(response.data);  // Save response data to state
      })
      .catch(error => {
        setError('Error fetching data from Django API');
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h1>Residents</h1>
      {error && <p>{error}</p>}
      <ul>
        {residents.map(resident => (
          <li key={resident.id}>
            {resident.name} (Room {resident.room_number})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TestAPI;
