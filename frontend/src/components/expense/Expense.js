import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Expense.css';
import Form from './Form';
import api from '../../api';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [selectedExpenseId, setSelectedExpenseId] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [newExpense, setNewExpense] = useState({
    description: '',
    cost: '',
    date: '',
  });

  useEffect(() => {
    api.get('api/expenses/')
      .then(response => {
        const sortedData = response.data.sort((exp1, exp2) => {
          return new Date(exp2.date) - new Date(exp1.date);
        });
        setExpenses(sortedData);
      })
      .catch(error => {
        console.error('Error fetching expenses:', error);
      });
  }, []);

  const handleRowClick = (expenseId) => {
    if(expenseId == selectedExpenseId) {
      setSelectedExpenseId(null);
    } else {
      setSelectedExpenseId(expenseId);
    }
    console.log(selectedExpenseId);
  };

  // Mega smart
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewExpense((prevExpense) => ({
      ...prevExpense,
      [name]: value, // Computed Property Name
    }));
  };

  const addExpense = (e) => {
    e.preventDefault();
    api.post('api/expenses/', newExpense)
      .then(response => {
        setExpenses([...expenses, response.data]);
        setShowForm(false);
        setNewExpense({ description: '', cost: '', date: '' });
        console.log('Expense added successfully!');
      })
      .catch(error => {
        console.error('Error adding expense:', error);
      });
  };

  const deleteExpense = (id) => {
    api.delete(`api/expenses/${id}/`)
        .then(response => {
          setExpenses(expenses.filter(expense => expense.id !== id));
          setSelectedExpenseId(null)
          console.log('Expense deleted successfully');
        })
        .catch(error => {
          console.error('Error deleting expense:', error);
        });
  }

  return (
    <div className="expense-table-container">
      <h1>Expenses</h1>
      <button className="addExpenseButton" onClick={() => setShowForm(!showForm)}>
          Add expense
      </button>
      {showForm && 
        <Form
          addExpense = {addExpense}
          newExpense = {newExpense}
          handleInputChange = {handleInputChange}
        />}
      {selectedExpenseId !== null && (
          <button className="deleteExpenseButton" onClick={() => deleteExpense(selectedExpenseId)}>
              Delete expense
          </button>
      )}

      <table className="expense-table">
        <thead>
          <tr>
            <th>Description</th>
            <th>Cost</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr
              key={expense.id}
              className={selectedExpenseId === expense.id ? 'selected' : ''}
              onClick={() => handleRowClick(expense.id)}
            >
              <td>{expense.description}</td>
              <td>{expense.cost} kr.</td>
              <td>{expense.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Expenses;
