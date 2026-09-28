import re

with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', index_content, re.DOTALL)
voice_nav_code = voice_nav_match.group(1) if voice_nav_match else ""

alerts_html = f"""<!DOCTYPE html>
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
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background-color: #cbd5e1; border-radius: 10px; }}
        @keyframes fade-in {{ from {{ opacity: 0; transform: translateY(-5px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-fade-in {{ animation: fade-in 0.4s ease-out forwards; }}
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans h-screen w-screen overflow-hidden m-0 p-0">
    <div id="root" class="h-full w-full"></div>
    
    <script type="text/babel">
{voice_nav_code}

function AlertsApp() {{
    const [alerts, setAlerts] = React.useState([]);
    const [loading, setLoading] = React.useState(true);
    const [selectedAlert, setSelectedAlert] = React.useState(null);
    const [toastAlert, setToastAlert] = React.useState(null);
    const seenAlerts = React.useRef(new Set());
    
    React.useEffect(() => {{
        if (alerts && alerts.length > 0) {{
            const latest = alerts[0];
            if (!seenAlerts.current.has(latest.id)) {{
                if (seenAlerts.current.size > 0) {{
                    setToastAlert(latest);
                    setTimeout(() => setToastAlert(null), 8000);
                }}
                alerts.forEach(a => seenAlerts.current.add(a.id));
            }}
        }}
    }}, [alerts]);

    const fetchAlerts = async () => {{
        try {{
            const res = await fetch('/api/v1/alerts');
            const data = await res.json();
            setAlerts(data.alerts || []);
        }} catch (e) {{
            console.error('Error fetching alerts');
        }}
        setLoading(false);
    }};

    React.useEffect(() => {{
        fetchAlerts();
        const interval = setInterval(fetchAlerts, 5000);
        return () => clearInterval(interval);
    }}, []);

    const handleDelete = async (id) => {{
        if(!confirm("Clear this threat alert permanently?")) return;
        try {{
            await fetch(`/api/v1/alerts/${{id}}`, {{ method: 'DELETE' }});
            fetchAlerts();
            if(selectedAlert && selectedAlert.id === id) setSelectedAlert(null);
        }} catch(e) {{
            console.error("Error deleting alert.");
        }}
    }};

    const getBadgeColor = (type) => {{
        const t = (type || '').toLowerCase();
        if (t.includes('stolen')) return 'bg-rose-100 text-rose-700 border-rose-200 shadow-sm';
        if (t.includes('wanted')) return 'bg-amber-100 text-amber-700 border-amber-200 shadow-sm';
        if (t.includes('amber')) return 'bg-purple-100 text-purple-700 border-purple-200 shadow-sm';
        return 'bg-blue-100 text-blue-700 border-blue-200 shadow-sm';
    }};

    return (
        <div className="relative w-full h-full overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900">
            
            {{/* BACKGROUND ACCENTS */}}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-200/40 rounded-full blur-[120px] pointer-events-none"></div>

            {{/* TOAST NOTIFICATION */}}
            {{toastAlert && (
                <div className="absolute top-32 left-1/2 transform -translate-x-1/2 z-[9999] bg-white rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] border border-rose-100 overflow-hidden flex animate-bounce flex-col w-[450px]">
                    <div className="bg-gradient-to-r from-rose-500 to-red-500 text-white px-5 py-3 font-black tracking-widest text-sm flex items-center justify-between">
                        <div className="flex items-center">
                            <span className="w-2.5 h-2.5 bg-white rounded-full animate-ping mr-3 shadow-lg"></span>
                            CRITICAL THREAT DETECTED
                        </div>
                        <button onClick={{() => setToastAlert(null)}} className="text-white/80 hover:text-white font-bold text-lg leading-none">&times;</button>
                    </div>
                    <div className="p-6 flex">
                        <div className="mr-5 text-rose-500 flex items-center justify-center">
                            <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        </div>
                        <div className="flex-1">
                            <div className="text-2xl font-black text-gray-900 font-mono tracking-wider mb-1">{{toastAlert.plate_number}}</div>
                            <div className="text-xs font-bold text-rose-600 mb-2 uppercase tracking-wide bg-rose-50 inline-block px-2 py-0.5 rounded border border-rose-100">{{toastAlert.alert_type}}</div>
                            <div className="text-sm font-medium text-gray-600 mb-3">{{toastAlert.description}}</div>
                            <div className="flex items-center justify-between mt-4">
                                <div className="text-xs font-bold text-gray-400 bg-gray-50 px-2 py-1 rounded">ID: {{toastAlert.camera_id}}</div>
                                <div className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{new Date(toastAlert.timestamp).toLocaleTimeString()}}</div>
                            </div>
                        </div>
                    </div>
                </div>
            )}}

            {{/* FLOATING TOP NAVIGATION BAR */}}
            <div className="absolute top-10 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex space-x-2">
                        <a href="/" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                        <a href="/tracking" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                        <a href="/blacklist" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                        <a href="/geofence" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                        <a href="/chat" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                        <a href="/alerts" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-rose-500 to-red-500 text-white shadow-lg shadow-rose-500/30 transition-transform transform hover:-translate-y-0.5">Alerts</a>
                    </div>
                </div>
            </div>

            {{/* MAIN CONTENT AREA */}}
            <div className="absolute top-32 left-6 right-6 bottom-6 flex gap-6 z-[900]">
                
                {{/* LEFT COLUMN: ALERTS LIST */}}
                <div className="w-full lg:w-2/3 h-full flex flex-col bg-white/90 backdrop-blur-3xl rounded-[22px] shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-100 bg-white/50 flex justify-between items-center">
                        <div>
                            <h2 className="text-2xl font-black text-gray-900 tracking-tight flex items-center">
                                <span className="w-2.5 h-2.5 rounded-full bg-rose-500 mr-2 shadow-[0_0_8px_rgba(244,63,94,0.8)] animate-pulse"></span>
                                Incident Log
                            </h2>
                            <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Real-time threat telemetry</p>
                        </div>
                        <div className="text-[10px] font-black uppercase tracking-widest text-indigo-500 bg-indigo-50 px-4 py-2 rounded-xl">
                            {{alerts.length}} Events Recorded
                        </div>
                    </div>
                    
                    <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
                        {{loading ? (
                            <div className="flex justify-center items-center h-40">
                                <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
                            </div>
                        ) : alerts.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                                <svg className="w-16 h-16 mb-4 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                <p className="font-bold uppercase tracking-widest text-xs">No active alerts</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {{alerts.map((alert, i) => (
                                    <div key={{alert.id}} onClick={{() => setSelectedAlert(alert)}} 
                                         className={{`cursor-pointer border-2 rounded-2xl p-4 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg animate-fade-in ${{selectedAlert?.id === alert.id ? 'border-rose-400 bg-rose-50/30' : 'border-gray-100 bg-white hover:border-rose-200'}}`}} 
                                         style={{{{ animationDelay: `${{i * 0.05}}s` }}}}>
                                        <div className="flex justify-between items-start mb-3">
                                            <div className="font-mono font-black text-gray-900 tracking-wider text-lg">
                                                {{alert.plate_number}}
                                            </div>
                                            <div className={{`text-[9px] font-black uppercase tracking-widest px-2 py-1 rounded-md border ${{getBadgeColor(alert.alert_type)}}`}}>
                                                {{alert.alert_type}}
                                            </div>
                                        </div>
                                        <div className="flex items-center text-xs font-bold text-gray-500 mb-4 bg-gray-50 rounded-lg p-2 border border-gray-100 inline-block">
                                            <svg className="w-3.5 h-3.5 mr-1.5 inline text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                            {{alert.camera_id}}
                                        </div>
                                        <div className="flex justify-between items-end border-t border-gray-50 pt-3">
                                            <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                                                {{new Date(alert.timestamp).toLocaleDateString()}}
                                            </div>
                                            <div className="text-[11px] font-black text-indigo-600 bg-indigo-50 px-2 py-1 rounded-md">
                                                {{new Date(alert.timestamp).toLocaleTimeString()}}
                                            </div>
                                        </div>
                                    </div>
                                ))}}
                            </div>
                        )}}
                    </div>
                </div>

                {{/* RIGHT COLUMN: ALERT DOSSIER */}}
                <div className="hidden lg:flex w-1/3 h-full flex-col">
                    {{selectedAlert ? (
                        <div className="w-full h-full bg-gradient-to-b from-rose-50 to-white rounded-[22px] shadow-sm border border-rose-100 overflow-hidden flex flex-col relative animate-fade-in">
                            {{/* Decorative Header Accent */}}
                            <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-rose-500 to-red-500"></div>
                            
                            <div className="p-8 pb-4 border-b border-rose-100/50">
                                <h3 className="text-[10px] font-black text-rose-500 uppercase tracking-widest mb-2 flex items-center">
                                    <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                    Threat Dossier
                                </h3>
                                <div className="text-4xl font-mono font-black text-gray-900 tracking-widest mb-4">
                                    {{selectedAlert.plate_number}}
                                </div>
                                <div className={{`inline-flex items-center text-xs font-black uppercase tracking-widest px-3 py-1.5 rounded-lg border ${{getBadgeColor(selectedAlert.alert_type)}}`}}>
                                    {{selectedAlert.alert_type}}
                                </div>
                            </div>
                            
                            <div className="flex-1 overflow-y-auto p-8 pt-6 space-y-6">
                                <div>
                                    <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 border-b border-gray-100 pb-1">Detection Node</h4>
                                    <p className="text-sm font-black text-gray-800 flex items-center bg-white p-3 rounded-xl border border-gray-100 shadow-sm">
                                        <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2 animate-pulse"></span>
                                        {{selectedAlert.camera_id}}
                                    </p>
                                </div>
                                
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 border-b border-gray-100 pb-1">Date</h4>
                                        <p className="text-sm font-bold text-gray-800">{{new Date(selectedAlert.timestamp).toLocaleDateString()}}</p>
                                    </div>
                                    <div>
                                        <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 border-b border-gray-100 pb-1">Time</h4>
                                        <p className="text-sm font-black text-indigo-600">{{new Date(selectedAlert.timestamp).toLocaleTimeString()}}</p>
                                    </div>
                                </div>
                                
                                <div>
                                    <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 border-b border-gray-100 pb-1">Intelligence Report</h4>
                                    <div className="bg-white p-4 rounded-xl border border-rose-100 shadow-sm relative">
                                        <svg className="absolute top-2 right-2 w-10 h-10 text-rose-50 opacity-50" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L1 21h22L12 2zm0 4.5l7.5 13h-15L12 6.5zM11 10v5h2v-5h-2zm0 7v2h2v-2h-2z"/></svg>
                                        <p className="text-sm font-medium text-gray-700 relative z-10 leading-relaxed">{{selectedAlert.description || 'No additional intelligence provided.'}}</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div className="p-6 bg-white border-t border-rose-100 mt-auto">
                                <button onClick={{() => handleDelete(selectedAlert.id)}} 
                                        className="w-full bg-rose-50 hover:bg-rose-500 text-rose-600 hover:text-white border-2 border-rose-100 hover:border-rose-500 py-3.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all shadow-sm hover:shadow-[0_0_15px_rgba(244,63,94,0.4)] flex justify-center items-center">
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                    Clear Threat Record
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="w-full h-full bg-white/40 backdrop-blur-md rounded-[22px] border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400">
                            <svg className="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                            <p className="font-bold uppercase tracking-widest text-xs">Select an incident to view dossier</p>
                        </div>
                    )}}
                </div>

            </div>
        </div>
    );
}}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<AlertsApp />);
</script>
</body>
</html>"""

with open("alerts.html", "w", encoding="utf-8") as f:
    f.write(alerts_html)

print("Rewrote alerts.html successfully!")
