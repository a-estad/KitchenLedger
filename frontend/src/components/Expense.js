import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/expenses/')
      .then(response => {
        setExpenses(response.data);
      })
      .catch(error => {
        console.error('Error fetching expenses:', error);
      });
  }, []);

  return (
    <div>
      <h1>Expenses</h1>
      <ul>
        {expenses.map(expense => (
          <li key={expense.id}>
            {expense.description} - ${expense.cost} on {expense.date}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Expenses;
