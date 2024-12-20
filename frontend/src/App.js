import React from 'react';
import './App.css'
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Debts from './pages/Debts';
import DinnerClubs from './pages/DinnerClubs';
import GeneralExpenses from './pages/GeneralExpense';

function App() {
  const location = useLocation();

  if (location.pathname === '/login' || location.pathname === '/register') {
    return (
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
      </Routes>
    );
  }

  return (
    <div className='root-div'>
      <Sidebar />
      <div className='content-of-pages'>
        <Routes>
          <Route path="/home" element={<ProtectedRoute> <Home/> </ProtectedRoute>} />
          <Route path="/expenses" element={<ProtectedRoute> <GeneralExpenses/> </ProtectedRoute> } />
          <Route path="/dinnerClubs" element={<ProtectedRoute> <DinnerClubs/> </ProtectedRoute>} />
          <Route path="/debts" element={<ProtectedRoute> <Debts/> </ProtectedRoute>} />
        </Routes>
      </div>
    </div>
  );
}

export default function MainApp() {
  return (
    <Router>
      <App />
    </Router>
  );
}
