import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Tracking from './pages/Tracking';
import Blacklist from './pages/Blacklist';
import Geofence from './pages/Geofence';
import Chat from './pages/Chat';
import Alerts from './pages/Alerts';
import Database from './pages/Database';
import Login from './pages/Login';
import Videos from './pages/Videos';

const PrivateRoute = ({ children }) => {
    return localStorage.getItem('nextra_token') ? children : <Navigate to="/login" replace />;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/tracking" element={<PrivateRoute><Tracking /></PrivateRoute>} />
        <Route path="/blacklist" element={<PrivateRoute><Blacklist /></PrivateRoute>} />
        <Route path="/geofence" element={<PrivateRoute><Geofence /></PrivateRoute>} />
        <Route path="/chat" element={<PrivateRoute><Chat /></PrivateRoute>} />
        <Route path="/alerts" element={<PrivateRoute><Alerts /></PrivateRoute>} />
        <Route path="/database" element={<PrivateRoute><Database /></PrivateRoute>} />
        <Route path="/videos" element={<PrivateRoute><Videos /></PrivateRoute>} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
