import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TestAPI from './components/TestAPI';
import Sidebar from './components/Sidebar';
import Expenses from './components/Expense';
import Residents from './components/Residents';

function App() {
  return (
    <Router>
      <div style={{ display: 'flex' }}>
        <Sidebar />
        <div style={{ marginLeft: '200px', padding: '20px', width: '100%' }}>
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
