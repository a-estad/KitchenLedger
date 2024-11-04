// ResidentBalances.js
import React, { useEffect, useState } from 'react';
import api from '../api';
import Modal from 'react-modal';

// Make sure to set the root element for accessibility
Modal.setAppElement('#root');

function ResidentBalances() {
    const [residentsData, setResidentsData] = useState([]);
    const [selectedResident, setSelectedResident] = useState(null);
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [selectedColumn, setSelectedColumn] = useState(null);

    useEffect(() => {
        fetchResidentBalances();
    }, []);

    const fetchResidentBalances = async () => {
        try {
            const response = await api.get('/api/balances/');
            console.log(response.data);
            setResidentsData(response.data);
        } catch (error) {
            console.error("Error fetching resident balances:", error);
        }
    };

    const openModal = (resident, selectedCol) => {
        setSelectedResident(resident);
        setSelectedColumn(selectedCol)
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
        setSelectedResident(null);
    };

    return (
        <div className="Debts-container">
            <h1>Debts</h1>
            <table>
                <thead>
                    <tr>
                        <th>Resident</th>
                        <th>General expenses</th>
                        <th>Total Paid</th>
                        <th>Dinne Clubs</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    {residentsData.map((resident, index) => (
                        <tr key={index}>
                            <td>{resident.resident}</td>
                            <td>{resident.generalExpensesTotal}</td>
                            <td onClick={() => openModal(resident, "General Expenses")} style={{ cursor: 'pointer', color: 'blue' }}>
                                {resident.paidFor}
                            </td>
                            <td>{resident.dinnerClubsTotal}</td>
                            <td>{resident.balance}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                contentLabel={selectedColumn}
                // TODO: Put styles in a css file
                style={{
                    content: {
                        top: '50%',
                        left: '50%',
                        right: 'auto',
                        bottom: 'auto',
                        marginRight: '-50%',
                        transform: 'translate(-50%, -50%)',
                        width: '500px',
                        padding: '20px',
                    },
                    overlay: {
                        backgroundColor: 'rgba(0, 0, 0, 0.75)'
                    }
                }}
            >
                {console.log(selectedResident)}
                <h2>{selectedColumn} for {selectedResident?.resident}</h2>
                {selectedResident && selectedResident.expensesPaidFor.length != 0 ? (
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Cost</th>
                            </tr>
                        </thead>
                        <tbody>
                            {selectedResident.expensesPaidFor.map((detail, index) => (
                                <tr key={index}>
                                    <td>{detail.date}</td>
                                    <td>{detail.description}</td>
                                    <td>{detail.cost}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No dinner club details available.</p>
                )}
            </Modal>

        </div>
    );
}

export default ResidentBalances;
