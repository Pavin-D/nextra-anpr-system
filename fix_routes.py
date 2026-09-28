import os
import re

pages_dir = "frontend/src/pages"
for filename in os.listdir(pages_dir):
    if filename.endswith(".jsx"):
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove the secure routing block
        pattern = r"\s*// --- SECURE ROUTING ---\s*if \(!localStorage\.getItem\('nextra_token'\)\) \{\s*window\.location\.href = '/login';\s*\}"
        new_content = re.sub(pattern, "", content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Cleaned {filename}")

app_jsx = """import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Tracking from './pages/Tracking';
import Blacklist from './pages/Blacklist';
import Geofence from './pages/Geofence';
import Chat from './pages/Chat';
import Alerts from './pages/Alerts';
import Database from './pages/Database';
import Login from './pages/Login';

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
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
"""
with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write(app_jsx)
print("Updated App.jsx")

