import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Home</h1>
      <Link to="/login">Login</Link> | <Link to="/register">Register</Link> | <Link to="/tasks">Tasks</Link>
    </div>
  );
};

export default Home;