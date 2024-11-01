import React, { useEffect, useState } from 'react';
import api from '../api';

function ResidentBalances() {
    const [residentsData, setResidentsData] = useState([]);

    useEffect(() => {
        fetchResidentBalances()
    }, []);

    const fetchResidentBalances = async () => {
        try {
            const response = await api.get('/api/balances/');
            setResidentsData(response.data);
        } catch (error) {
            console.error("Error fetching resident balances:", error);
        }
    };


    return <div className="Debts-container">
        <h1>Debts</h1>
        <table>
            <thead>
                <tr>
                    <th>Resident</th>
                    <th>General expenses</th>
                    <th>Dinner club expenses</th>
                    <th>Total Paid</th>
                    <th>Balance</th>
                </tr>
            </thead>
            <tbody>
                {residentsData.map((resident, index) => (
                    <tr key={index}>
                        <td>{resident.resident}</td>
                        <td>{resident.non_dinner_club_total}</td>
                        <td>{resident.dinner_club_total}</td>
                        <td>{resident.paidFor}</td>
                        <td>{resident.balance}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default ResidentBalances