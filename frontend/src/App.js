import React from 'react';
import './App.css'
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
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
  return (
    <Router>
      <div className='root-div'>
        <Sidebar />
        <div className='content-of-pages'>
          <Routes>
            <Route path="/login" element={<Login/>} />
            <Route path="/register" element={<Register/>} />
            <Route path="/home" element={<ProtectedRoute> <Home/> </ProtectedRoute>} />
            <Route path="/expenses" element={<Expenses/> } />
            <Route path="/residents" element={<ProtectedRoute> <Residents/> </ProtectedRoute>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
