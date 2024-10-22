import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
        <nav>
            <ul>
                <li className='active'><Link to="/">Home</Link></li>
                <li><Link to="/expenses">Expenses</Link></li>
                <li><Link to="/residents">Residents</Link></li>
            </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
