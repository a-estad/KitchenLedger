import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Expense.css';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [selectedExpenseId, setSelectedExpenseId] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [newExpense, setNewExpense] = useState({
    description: '',
    cost: '',
    date: '',
    paid_by: '',
    is_dinner_club: false,
  });

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/expenses/')
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
    const { name, value, type, checked } = e.target;
    setNewExpense((prevExpense) => ({
      ...prevExpense,
      [name]: type === 'checkbox' ? checked : value, // Computed Property Name
    }));
  };

  const addExpense = (e) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8000/api/expenses/', newExpense)
      .then(response => {
        setExpenses([...expenses, response.data]);
        setShowForm(false);
        setNewExpense({ description: '', cost: '', date: '', paid_by: '', is_dinner_club: false });
        console.log('Expense added successfully!');
      })
      .catch(error => {
        console.error('Error adding expense:', error);
      });
  };

  const deleteExpense = (id) => {
    axios.delete(`http://127.0.0.1:8000/api/expenses/${id}/`)
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
      {showForm && (
        <form onSubmit={addExpense}>
          <div>
            <label>Description:</label>
            <input
              type="text"
              name="description"
              value={newExpense.description}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label>Cost:</label>
            <input
              type="number"
              name="cost"
              value={newExpense.cost}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label>Date:</label>
            <input
              type="date"
              name="date"
              value={newExpense.date}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label>Paid by (Resident ID):</label>
            <input
              type="text"
              name="paid_by"
              value={newExpense.paid_by}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label>
              Is Dinner Club:
              <input
                type="checkbox"
                name="is_dinner_club"
                checked={newExpense.is_dinner_club}
                onChange={handleInputChange}
              />
            </label>
          </div>

          <button type="submit">Create Expense</button>
        </form>)}
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
