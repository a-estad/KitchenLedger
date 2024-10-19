import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div style={{
      width: '200px',
      height: '100vh',
      backgroundColor: '#f4f4f4',
      padding: '10px',
      position: 'fixed',
    }}>
      <h2>Menu</h2>
      <ul style={{ listStyleType: 'none', padding: '0' }}>
        <li><Link to="/expenses">Expenses</Link></li>
        <li><Link to="/residents">Residents</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
