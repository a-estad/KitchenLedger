import React, { useState, useEffect } from 'react';
import api from '../api';
import Form from '../components/DinnerclubForm';
import '../styles/Table.css';

function DinnerClubs() {
    const [dinnerClubs, setDinnerClubs] = useState([]);
    const [newDinnerclub, setNewDinnerClub] = useState({
        description: '',
        cost: '',
        date: '',
        roomNumbers: '',
    });
    const [showForm, setShowForm] = useState(false);
    const [selectedDinnerclubId, setSelectedDinnerclubId] = useState(null);


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

    const handleRowClick = (dinnerclubId) => {
        if(dinnerclubId == selectedDinnerclubId) {
            setSelectedDinnerclubId(null);
        } else {
            setSelectedDinnerclubId(dinnerclubId);
        }
        console.log(selectedDinnerclubId);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewDinnerClub((prevDinnerClub) => ({
            ...prevDinnerClub,
            [name]: value, // Computed Property Name
        }));
    };

    const deleteDinnerclub = (id) => {
        api.delete(`api/dinnerclubs/${id}/`)
            .then(response => {
              setDinnerClubs(dinnerClubs.filter(dinnerClubs => dinnerClubs.id !== id));
              setSelectedDinnerclubId(null)
              console.log('Dinnerclub deleted successfully');
            })
            .catch(error => {
              console.error('Error deleting Dinnerclub:', error);
            });
      }

    const addDinnerclub = async (e) => {
        e.preventDefault();

        // Convert comma-separated room numbers into an array
        const participantsRoomNumbers = newDinnerclub.roomNumbers
            .split(',')
            .map(room => room.trim())
            .filter(room => room !== '');

        const data = {
            expense: {
                description: newDinnerclub.description,
                cost: newDinnerclub.cost,
                date: newDinnerclub.date,
                is_dinner_club: true,
            },
            participantsRoomNumbers: participantsRoomNumbers,
        };

        try {
            const response = await api.post('/api/dinnerclubs/', data);
            setDinnerClubs([...dinnerClubs, response.data]);
            console.log('DinnerClub created:', response.data);
            setNewDinnerClub({
                description: '',
                cost: '',
                date: '',
                roomNumbers: '',
            });
        } catch (error) {
            console.error('Error creating DinnerClub:', error);
        }
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
            {selectedDinnerclubId !== null && (
                <button onClick={() => deleteDinnerclub(selectedDinnerclubId)}>
                    Delete dinnerclub
                </button>
            )}
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
                {dinnerClubs.map((dinnerClub) => (
                <tr
                    key={dinnerClub.id}
                    className={selectedDinnerclubId === dinnerClub.id ? 'selected' : ''}
                    onClick={() => handleRowClick(dinnerClub.id)}
                >
                    <td>{dinnerClub.expense.date}</td>
                    <td>{dinnerClub.expense.description}</td>
                    <td>{dinnerClub.participants.length}</td>
                    <td>{dinnerClub.expense.cost} kr</td>
                </tr>
                ))}
                </tbody>
            </table>
        </div>
        
    )
}

export default DinnerClubs