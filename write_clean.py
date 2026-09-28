html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - Threat Alerts Log</title>
    <!-- React & Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .glass-panel { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        .row-enter { animation: fade-in 0.3s ease-out forwards; }
        @keyframes fade-in { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-gradient-to-br from-gray-50 to-gray-100 text-gray-900 font-sans min-h-screen">
    <div id="root"></div>
    
    <script type="text/babel">
        function AlertsApp() {
            const [alerts, setAlerts] = React.useState([]);
            const [loading, setLoading] = React.useState(true);
            const [selectedAlert, setSelectedAlert] = React.useState(null);
            
            // TOAST LOGIC
            const [toastAlert, setToastAlert] = React.useState(null);
            const seenAlerts = React.useRef(new Set());
            
            React.useEffect(() => {
                if (alerts && alerts.length > 0) {
                    const latest = alerts[0];
                    if (!seenAlerts.current.has(latest.id)) {
                        if (seenAlerts.current.size > 0) {
                            setToastAlert(latest);
                            setTimeout(() => setToastAlert(null), 8000);
                        }
                        alerts.forEach(a => seenAlerts.current.add(a.id));
                    }
                }
            }, [alerts]);

            const fetchAlerts = async () => {
                try {
                    const res = await fetch('/api/v1/alerts');
                    const data = await res.json();
                    setAlerts(data.alerts || []);
                } catch (e) {
                    console.error('Error fetching alerts');
                }
                setLoading(false);
            };

            React.useEffect(() => {
                fetchAlerts();
                const interval = setInterval(fetchAlerts, 5000); // Auto-refresh every 5s
                return () => clearInterval(interval);
            }, []);

            const handleDelete = async (id) => {
                if(!confirm("Clear this threat alert permanently?")) return;
                try {
                    await fetch(`/api/v1/alerts/${id}`, { method: 'DELETE' });
                    fetchAlerts();
                    if(selectedAlert && selectedAlert.id === id) setSelectedAlert(null);
                } catch(e) {
                    console.error("Error deleting alert.");
                }
            };

            const getBadgeColor = (type) => {
                const t = (type || '').toLowerCase();
                if (t.includes('stolen')) return 'bg-rose-100 text-rose-700 border-rose-200 shadow-[0_0_10px_rgba(244,63,94,0.3)]';
                if (t.includes('wanted')) return 'bg-amber-100 text-amber-700 border-amber-200 shadow-[0_0_10px_rgba(245,158,11,0.3)]';
                if (t.includes('amber')) return 'bg-purple-100 text-purple-700 border-purple-200 shadow-[0_0_10px_rgba(168,85,247,0.3)]';
                return 'bg-blue-100 text-blue-700 border-blue-200';
            };

            return (
                <div className="flex flex-col min-h-screen">
                    {/* TOAST NOTIFICATION */}
                    {toastAlert && (
                        <div className="absolute top-24 left-1/2 transform -translate-x-1/2 z-[9999] bg-white rounded-2xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] border-2 border-rose-500 overflow-hidden flex animate-bounce flex-col w-[450px]">
                            <div className="bg-rose-500 text-white px-4 py-2 font-black tracking-widest text-sm flex items-center justify-between">
                                <div className="flex items-center">
                                    <span className="w-2.5 h-2.5 bg-white rounded-full animate-ping mr-3"></span>
                                    THREAT DETECTED
                                </div>
                                <button onClick={() => setToastAlert(null)} className="text-white/80 hover:text-white">&times;</button>
                            </div>
                            <div className="p-5 flex">
                                <div className="mr-4 text-rose-500">
                                    <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                </div>
                                <div>
                                    <div className="text-xl font-black text-gray-900 font-mono tracking-wider mb-1">{toastAlert.plate_number}</div>
                                    <div className="text-sm font-bold text-rose-600 mb-2 uppercase tracking-wide">{toastAlert.alert_type}</div>
                                    <div className="text-xs text-gray-600 mb-2">{toastAlert.description}</div>
                                    <div className="inline-block bg-gray-100 text-gray-700 text-xs font-bold px-2 py-1 rounded">📍 {toastAlert.camera_id} @ {new Date(toastAlert.timestamp).toLocaleTimeString()}</div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* TOP NAVIGATION BAR */}
                    <div className="h-16 bg-white border-b border-gray-200 flex items-center px-6 justify-between shadow-sm flex-shrink-0 relative z-50">
                        <div className="flex items-center space-x-4">
                            <h1 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        </div>
                        <div className="hidden md:flex space-x-1 border border-gray-200 rounded-lg p-1 bg-gray-50">
                            <a href="/" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Dashboard Overview</a>
                            <a href="/tracking" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Vehicle Tracking</a>
                            <a href="/blacklist" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Blacklist Manager</a>
                            <a href="/geofence" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Geofence Analytics</a>
                            <a href="/chat" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">AI Chat Search</a>
                            <a href="/alerts" className="px-4 py-1.5 text-sm font-bold rounded-md bg-white text-rose-600 shadow-sm border border-rose-100">Threat Alerts</a>
                        </div>
                    </div>

                    {/* MAIN CONTENT */}
                    <div className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col">
                        
                        {/* HEADER */}
                        <div className="mb-8 flex justify-between items-end">
                            <div>
                                <h2 className="text-3xl font-black text-gray-900 tracking-tight mb-2 flex items-center">
                                    <span className="bg-rose-500 text-white p-2 rounded-xl mr-3 shadow-lg shadow-rose-500/30 animate-pulse">
                                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                    </span>
                                    System Threat Log
                                </h2>
                                <p className="text-gray-500 font-medium ml-12">Automated logs for all blacklisted and flagged vehicles detected by the AI.</p>
                            </div>
                            <div className="bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm flex items-center text-sm font-bold text-gray-700">
                                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 mr-2 animate-ping"></div>
                                Live Monitoring Active
                            </div>
                        </div>

                        {/* SPLIT LAYOUT: TABLE + DOSSIER */}
                        <div className="flex flex-row flex-1 overflow-hidden">
                            {/* TABLE SECTION */}
                            <div className={`bg-white rounded-3xl shadow-[0_10px_40px_rgba(0,0,0,0.04)] border border-gray-100 overflow-hidden flex flex-col transition-all duration-500 ease-in-out ${selectedAlert ? 'w-2/3 mr-6' : 'w-full'}`}>
                                <div className="overflow-auto flex-1 p-0">
                                    <table className="w-full text-left border-collapse">
                                        <thead className="bg-gray-50/90 backdrop-blur-md sticky top-0 z-10 border-b border-gray-100">
                                            <tr>
                                                <th className="px-6 py-5 text-xs font-black text-indigo-300 uppercase tracking-widest">Plate</th>
                                                <th className="px-6 py-5 text-xs font-black text-indigo-300 uppercase tracking-widest">Type</th>
                                                <th className="px-6 py-5 text-xs font-black text-indigo-300 uppercase tracking-widest">Node</th>
                                                <th className="px-6 py-5 text-xs font-black text-indigo-300 uppercase tracking-widest">Time</th>
                                                <th className="px-6 py-5 text-xs font-black text-indigo-300 uppercase tracking-widest text-right">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-50">
                                            {loading ? (
                                                <tr><td colSpan="5" className="px-8 py-16 text-center text-gray-400 font-bold text-lg animate-pulse">Scanning logs...</td></tr>
                                            ) : alerts.length === 0 ? (
                                                <tr><td colSpan="5" className="px-8 py-16 text-center text-gray-400 font-medium">No threats detected.</td></tr>
                                            ) : (
                                                alerts.map((alert) => (
                                                    <tr key={alert.id} className={`transition-all duration-300 group cursor-pointer ${selectedAlert?.id === alert.id ? 'bg-indigo-50/50 shadow-inner' : 'hover:bg-gray-50/80'} row-enter`} onClick={() => setSelectedAlert(alert)}>
                                                        <td className="px-6 py-5">
                                                            <div className={`font-mono font-black text-lg tracking-wider inline-block px-3 py-1.5 rounded-lg border shadow-sm ${selectedAlert?.id === alert.id ? 'bg-indigo-600 text-white border-indigo-700' : 'text-indigo-700 bg-white border-indigo-100'}`}>{alert.plate_number}</div>
                                                        </td>
                                                        <td className="px-6 py-5">
                                                            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wider ${getBadgeColor(alert.alert_type)}`}>
                                                                <span className="w-1.5 h-1.5 rounded-full bg-current mr-2 animate-pulse"></span>
                                                                {alert.alert_type}
                                                            </span>
                                                        </td>
                                                        <td className="px-6 py-5 text-sm font-bold text-gray-600">
                                                            <div className="flex items-center">
                                                                <svg className="w-4 h-4 mr-2 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                                {alert.camera_id}
                                                            </div>
                                                        </td>
                                                        <td className="px-6 py-5 text-sm font-semibold text-gray-500">
                                                            {new Date(alert.timestamp).toLocaleTimeString()}
                                                        </td>
                                                        <td className="px-6 py-5 text-right">
                                                            <button onClick={(e) => { e.stopPropagation(); setSelectedAlert(alert); }} className="bg-indigo-50 text-indigo-600 hover:bg-indigo-600 hover:text-white px-4 py-2 rounded-lg font-bold text-xs uppercase tracking-wider transition-all shadow-sm mr-2 opacity-0 group-hover:opacity-100">
                                                                View
                                                            </button>
                                                            <button onClick={(e) => { e.stopPropagation(); handleDelete(alert.id); }} className="bg-rose-50 text-rose-600 hover:bg-rose-500 hover:text-white px-4 py-2 rounded-lg font-bold text-xs uppercase tracking-wider transition-all shadow-sm opacity-0 group-hover:opacity-100">
                                                                Dismiss
                                                            </button>
                                                        </td>
                                                    </tr>
                                                ))
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            
                            {/* SIDE DOSSIER PANEL */}
                            {selectedAlert && (
                                <div className="w-1/3 bg-white rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.08)] border border-gray-100 flex flex-col relative overflow-hidden animate-[fade-in_0.4s_ease-out_forwards]">
                                    <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-br from-gray-900 to-indigo-900 z-0"></div>
                                    <button onClick={() => setSelectedAlert(null)} className="absolute top-4 right-4 z-20 bg-white/20 hover:bg-white/40 text-white rounded-full p-2 transition-all">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                                    </button>
                                    
                                    <div className="relative z-10 pt-16 px-8 pb-8 flex-1 overflow-y-auto">
                                        <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-50 text-center mb-8">
                                            <div className="inline-block bg-rose-100 text-rose-600 p-3 rounded-full mb-3 shadow-inner">
                                                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                            </div>
                                            <h3 className="font-mono text-3xl font-black text-gray-900 tracking-widest mb-1">{selectedAlert.plate_number}</h3>
                                            <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${getBadgeColor(selectedAlert.alert_type)}`}>{selectedAlert.alert_type}</div>
                                        </div>

                                        <div className="space-y-6">
                                            <div>
                                                <div className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Detection Event</div>
                                                <div className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                                                    <div className="flex items-center justify-between mb-2">
                                                        <span className="text-sm font-semibold text-gray-500">Location</span>
                                                        <span className="text-sm font-black text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded">{selectedAlert.camera_id}</span>
                                                    </div>
                                                    <div className="flex items-center justify-between">
                                                        <span className="text-sm font-semibold text-gray-500">Time</span>
                                                        <span className="text-sm font-bold text-gray-800">{new Date(selectedAlert.timestamp).toLocaleString()}</span>
                                                    </div>
                                                </div>
                                            </div>

                                            <div>
                                                <div className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Blacklist Database Origin</div>
                                                <div className="bg-rose-50 rounded-xl p-4 border border-rose-100">
                                                    <div className="flex items-center justify-between mb-2">
                                                        <span className="text-sm font-semibold text-rose-800/60">Date Added</span>
                                                        <span className="text-sm font-black text-rose-700">{selectedAlert.blacklist_date ? new Date(selectedAlert.blacklist_date).toLocaleString() : 'Unknown (Legacy)'}</span>
                                                    </div>
                                                    <div className="flex flex-col">
                                                        <span className="text-sm font-semibold text-rose-800/60 mb-1">Original Reason / Notes</span>
                                                        <span className="text-sm font-semibold text-gray-800 bg-white p-3 rounded-lg border border-rose-100 shadow-sm">{selectedAlert.blacklist_reason || selectedAlert.description || 'No original notes provided.'}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<AlertsApp />);
    </script>
</body>
</html>"""

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Complete alerts.html successfully written.")
