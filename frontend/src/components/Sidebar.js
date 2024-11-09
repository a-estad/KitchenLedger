import { useState, React } from 'react';
import { Link, useLocation, Navigate } from 'react-router-dom';
import '../styles/Sidebar.css';

function Logout() {
  localStorage.clear()
  return (
    <Navigate to="/login"/>
  )
}

const Sidebar = () => {
  const [loggedOut, setLoggedOut] = useState(false);
  const location = useLocation();

  const handleLogout = () => {
    setLoggedOut(true);
  };

  return (
    <div className="sidebar">
      {loggedOut && <Logout />}
      <nav>
        <ul>
          <li>
            <Link to="/home" className={location.pathname === '/home' ? 'active' : ''}>Home</Link>
          </li>
          <li>
            <Link to="/expenses" className={location.pathname === '/expenses' ? 'active' : ''}>Expenses</Link>
          </li>
          <li>
            <Link to="/dinnerClubs" className={location.pathname === '/dinnerClubs' ? 'active' : ''}>Dinner Clubs</Link>
          </li>
          <li>
            <Link to="/debts" className={location.pathname === '/debts' ? 'active' : ''}>Debts</Link>
          </li>
        </ul>
      </nav>
      <button className='logout-btn' onClick={() => handleLogout()}>
        Logout
      </button>
    </div>
  );
};

export default Sidebar;
