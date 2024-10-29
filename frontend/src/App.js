import React from 'react';
import './App.css'
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import Sidebar from './components/sidebar/Sidebar';
import Expenses from './components/expense/Expense';
import Residents from './components/Residents';
import Login from './pages/Login';
import Register from './pages/Register';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';

function Logout() {
  localStorage.clear()
  return <Navigate to="/login"/>
}

function RegisterAndLogout() {
  localStorage()
  return <Register/>
}


function App() {
  const location = useLocation();

  if (location.pathname === '/login' || location.pathname === '/register') {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    );
  }

  return (
    <div className='root-div'>
      <Sidebar />
      <div className='content-of-pages'>
        <Routes>
          <Route path="/home" element={<ProtectedRoute> <Home/> </ProtectedRoute>} />
          <Route path="/expenses" element={<Expenses/> } />
          <Route path="/residents" element={<ProtectedRoute> <Residents/> </ProtectedRoute>} />
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
