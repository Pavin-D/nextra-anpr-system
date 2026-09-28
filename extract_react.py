import os
import re

html_files = {
    "index.html": "Dashboard",
    "tracking.html": "Tracking",
    "blacklist.html": "Blacklist",
    "geofence.html": "Geofence",
    "chat.html": "Chat",
    "alerts.html": "Alerts",
    "database.html": "Database",
    "login.html": "Login"
}

os.makedirs("frontend/src/pages", exist_ok=True)
os.makedirs("frontend/src/components", exist_ok=True)

all_styles = []

for file, component in html_files.items():
    if not os.path.exists(file): continue
    
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract styles
    styles = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
    for s in styles:
        all_styles.append(s)

    # Extract Babel script
    babel_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    if not babel_match: continue
    
    js_content = babel_match.group(1)
    
    # Remove ReactDOM.createRoot
    js_content = re.sub(r'const root = ReactDOM\.createRoot.*?;', '', js_content, flags=re.DOTALL)
    js_content = re.sub(r'root\.render\(.*?\);', '', js_content, flags=re.DOTALL)
    
    # Add imports
    imports = "import React, { useState, useEffect, useRef } from 'react';\n"
    
    # If VoiceNav is defined in this file, we can leave it. But it's defined multiple times.
    # To avoid React component export issues, we just add `export default function {app_name}()`
    
    # The main app function is usually named App, LoginApp, DashboardApp, etc.
    # We will find the function that is rendered by root.render
    render_match = re.search(r'root\.render\(<([A-Za-z0-9_]+) />\);', babel_match.group(1))
    if render_match:
        app_name = render_match.group(1)
        js_content = re.sub(f'function {app_name}', f'export default function {app_name}', js_content)
    else:
        # Fallback
        js_content += f"\nexport default {component}App;\n"

    # Save to pages
    with open(f"frontend/src/pages/{component}.jsx", "w", encoding="utf-8") as f:
        f.write(imports + js_content)

# Merge styles and write to index.css
unique_styles = []
for s in all_styles:
    if s.strip() not in unique_styles:
        unique_styles.append(s.strip())

with open("frontend/src/index.css", "a", encoding="utf-8") as f:
    f.write("\n" + "\n".join(unique_styles) + "\n")

# Create App.jsx with routing
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

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/tracking" element={<Tracking />} />
        <Route path="/blacklist" element={<Blacklist />} />
        <Route path="/geofence" element={<Geofence />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/database" element={<Database />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
"""
with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write(app_jsx)

print("Migration scripts extracted!")
