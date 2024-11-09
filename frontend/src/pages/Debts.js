// ResidentBalances.js
import React, { useEffect, useState } from 'react';
import api from '../api';
import Modal from 'react-modal';
import '../styles/Debts.css';
import '../styles/Table.css';

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
        setSelectedColumn(null);
    };

    return (
        <div className="debtsContainer">
            <h1>Debts</h1>
            <table className="coolTable">
                <thead>
                    <tr>
                        <th>Resident</th>
                        <th>General expenses</th>
                        <th>Dinne Clubs</th>
                        <th>Total Paid</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    {residentsData.map((resident, index) => (
                        <tr key={index}>
                            <td>{resident.resident}</td>
                            <td onClick={() => openModal(resident, "General Expenses")} style={{ cursor: 'pointer', color: 'blue' }}>
                                {-resident.generalExpensesTotal.toFixed(2)}
                            </td>
                            <td onClick={() => openModal(resident, "Dinner Club Debts")} style={{ cursor: 'pointer', color: 'blue' }}>
                                {-resident.dinnerClubsTotal.toFixed(2)}
                            </td>
                            <td onClick={() => openModal(resident, "Expenses Paid For")} style={{ cursor: 'pointer', color: 'blue' }}>
                                {resident.paidFor.toFixed(2)}
                            </td>
                            <td>{resident.balance.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                contentLabel={selectedColumn}
                className="modal-content"
                overlayClassName="modal-overlay"
            >
                {console.log(selectedResident)}
                <h2>{selectedColumn} for {selectedResident?.resident}</h2>
                {selectedResident && selectedColumn === "General Expenses" && selectedResident.generalExpensesDebts.length != 0 ? (
                    <table className="coolTable">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Expense total cost</th>
                                <th>Your share</th>
                            </tr>
                        </thead>
                        <tbody>
                            {selectedResident.generalExpensesDebts.map((debt, index) => (
                                <tr key={index}>
                                    <td>{debt.expense.date}</td>
                                    <td>{debt.expense.description}</td>
                                    <td>{debt.expense.cost.toFixed(2)}</td>
                                    <td>{debt.amount.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : selectedColumn === "Expenses Paid For" && selectedResident.expensesPaidFor.length !== 0 ? (
                    <table className="coolTable">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Cost</th>
                                <th>Dinner club</th>
                            </tr>
                        </thead>
                        <tbody>
                            {selectedResident.expensesPaidFor.map((expense, index) => (
                                <tr key={index}>
                                    <td>{expense.date}</td>
                                    <td>{expense.description}</td>
                                    <td>{expense.cost.toFixed(2)}</td>
                                    <td>{expense.is_dinner_club.toString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : selectedColumn === "Dinner Club Debts" && selectedResident.dinnerClubDebts.length !== 0 ? (
                    <table className="coolTable">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Cost</th>
                                <th>Amount Owed</th>
                            </tr>
                        </thead>
                        <tbody>
                            {selectedResident.dinnerClubDebts.map((debt, index) => (
                                <tr key={index}>
                                    <td>{debt.expense_date}</td>
                                    <td>{debt.description}</td>
                                    <td>{debt.cost.toFixed(2)}</td>
                                    <td>{debt.amount.toFixed(2)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : 
                (
                    <p>No {selectedColumn} details available.</p>
                )}
            </Modal>

        </div>
    );
}

export default ResidentBalances;
