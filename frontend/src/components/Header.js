// src/components/Header.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Header.css';   

function Header({ setIsAuthenticated }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    setIsAuthenticated(false);
    sessionStorage.removeItem('isAuthenticated');
    navigate('/login');
  };
  return (
    <header className={sessionStorage.getItem('isAuthenticated') ? 'header-login':'header'}>
      <h1>&lt;/&gt; CodeMate</h1>
    {sessionStorage.getItem('isAuthenticated') ?<button className="logout" onClick={handleLogout}>Logout</button>:''}

      
    </header>
  );
};


export default Header;
