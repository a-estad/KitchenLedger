import React, { useState, useEffect } from 'react';
import api from '../api';
import Form from '../components/DinnerclubForm';
import '../styles/Table.css';

function DinnerClubs() {
    const [dinnerClubs, setDinnerClubs] = useState([]);
    const [newDinnerclub, setNewDinnerClub] = useState([]);
    const [showForm, setShowForm] = useState(false);


    useEffect(() => {
        api.get('api/dinnerclubs/')
          .then(response => {
            console.log(response.data)
            // const sortedData = response.data.sort((dc1, dc2) => {
            //   return new Date(dc2.date) - new Date(dc1.date);
            // });
            setDinnerClubs(response.data);
          })
          .catch(error => {
            console.error('Error fetching dinner clubs:', error);
          });
      }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewDinnerClub((prevDinnerClub) => ({
            ...prevDinnerClub,
            [name]: value, // Computed Property Name
        }));
    };

    const addDinnerclub = (e) => {
        e.preventDefault();
        api.post('api/dinnerclubs/', newDinnerclub)
          .then(response => {
            setDinnerClubs([...dinnerClubs, response.data]);
            setShowForm(false);
            // setNewExpense({ description: '', cost: '', date: '' });
            console.log('Dinnerclub added successfully!');
          })
          .catch(error => {
            console.error('Error adding expense:', error);
          });
      };

    return (
        <div>
            <h1>Dinner Clubs</h1>
            <button onClick={() => setShowForm(!showForm)}>
                Add dinner club
            </button>
            {showForm && 
                <Form
                addDinnerclub = {addDinnerclub}
                newDinnerclub = {newDinnerclub}
                handleInputChange = {handleInputChange}
                />
            }
            <table className="coolTable">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Description</th>
                        <th>Number of participants</th>
                        <th>Cost</th>
                    </tr>
                </thead>
                <tbody>
                {dinnerClubs.map((dinnerClub, index) => (
                <tr
                    key={index}
                >
                    <td>{dinnerClub.date}</td>
                    <td>{dinnerClub.description}</td>
                    <td>{dinnerClub.cost} kr.</td>
                    <td>{dinnerClub.numberOfParticipants}</td>
                </tr>
                ))}
                </tbody>
            </table>
        </div>
        
    )
}

export default DinnerClubs