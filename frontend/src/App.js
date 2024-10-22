import React from 'react';
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/sidebar/Sidebar';
import Expenses from './components/expense/Expense';
import Residents from './components/Residents';

function App() {
  return (
    <Router>
      <div className='root-div'>
        <Sidebar />
        <div className='content-of-pages'>
          <Routes>
            <Route path="/expenses" element={<Expenses />} />
            <Route path="/residents" element={<Residents />} />
            {/* Add more routes for other models like Debts, Payments, etc. */}
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
