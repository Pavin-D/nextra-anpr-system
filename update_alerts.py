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

                        {/* TABLE SECTION */}
                        <div className="bg-white rounded-3xl shadow-2xl border border-gray-100 overflow-hidden flex flex-col flex-1">
                            <div className="overflow-auto flex-1 p-0">
                                <table className="w-full text-left border-collapse">
                                    <thead className="bg-gray-50/80 backdrop-blur sticky top-0 z-10 border-b border-gray-200">
                                        <tr>
                                            <th className="px-8 py-5 text-xs font-black text-gray-400 uppercase tracking-widest">Detected Plate</th>
                                            <th className="px-8 py-5 text-xs font-black text-gray-400 uppercase tracking-widest">Threat Level</th>
                                            <th className="px-8 py-5 text-xs font-black text-gray-400 uppercase tracking-widest">Camera Node</th>
                                            <th className="px-8 py-5 text-xs font-black text-gray-400 uppercase tracking-widest">Timestamp</th>
                                            <th className="px-8 py-5 text-xs font-black text-gray-400 uppercase tracking-widest text-right">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-50">
                                        {loading ? (
                                            <tr><td colSpan="5" className="px-8 py-16 text-center text-gray-400 font-bold text-lg animate-pulse">Scanning database...</td></tr>
                                        ) : alerts.length === 0 ? (
                                            <tr><td colSpan="5" className="px-8 py-16 text-center text-gray-400 font-medium">No threats detected in the system.</td></tr>
                                        ) : (
                                            alerts.map((alert) => (
                                                <tr key={alert.id} className="hover:bg-indigo-50/50 transition-colors group row-enter">
                                                    <td className="px-8 py-5">
                                                        <div className="font-mono font-black text-indigo-700 text-lg tracking-wider bg-white border border-indigo-100 shadow-sm inline-block px-3 py-1.5 rounded-lg">{alert.plate_number}</div>
                                                    </td>
                                                    <td className="px-8 py-5">
                                                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-wider ${getBadgeColor(alert.alert_type)}`}>
                                                            {alert.alert_type}
                                                        </span>
                                                        <div className="text-xs text-gray-500 font-medium mt-1 truncate max-w-xs">{alert.description}</div>
                                                    </td>
                                                    <td className="px-8 py-5 text-sm font-bold text-gray-700">
                                                        <div className="flex items-center bg-gray-100 w-max px-3 py-1 rounded-lg">
                                                            <svg className="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                            {alert.camera_id}
                                                        </div>
                                                    </td>
                                                    <td className="px-8 py-5 text-sm font-semibold text-gray-500">
                                                        {new Date(alert.timestamp).toLocaleString()}
                                                    </td>
                                                    <td className="px-8 py-5 text-right opacity-0 group-hover:opacity-100 transition-opacity">
                                                        <button onClick={() => handleDelete(alert.id)} className="bg-rose-50 text-rose-600 hover:bg-rose-500 hover:text-white px-4 py-2 rounded-lg font-bold text-xs uppercase tracking-wider transition-all shadow-sm">
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
print("Updated alerts.html completely.")
