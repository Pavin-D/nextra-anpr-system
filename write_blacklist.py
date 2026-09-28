import re

with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

# Extract VoiceNav
voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', index_content, re.DOTALL)
voice_nav_code = voice_nav_match.group(1) if voice_nav_match else ""

blacklist_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - Blacklist Management</title>
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
        @keyframes fade-in {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans h-screen w-screen overflow-hidden">
    <div id="root" class="h-full w-full"></div>
    
    <script type="text/babel">
{voice_nav_code}

function BlacklistApp() {{
    const [blacklist, setBlacklist] = React.useState([]);
    const [newPlate, setNewPlate] = React.useState('');
    const [newReason, setNewReason] = React.useState('');
    const [status, setStatus] = React.useState('');
    const [isSubmitting, setIsSubmitting] = React.useState(false);

    React.useEffect(() => {{
        fetchBlacklist();
    }}, []);

    const fetchBlacklist = async () => {{
        try {{
            const res = await fetch('/api/v1/blacklist');
            const data = await res.json();
            setBlacklist(data.blacklist || []);
        }} catch (e) {{
            console.error("Error fetching blacklist", e);
        }}
    }};

    const handleAdd = async (e) => {{
        e.preventDefault();
        if(!newPlate || !newReason) return;
        setIsSubmitting(true);
        try {{
            const res = await fetch('/api/v1/blacklist', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{plate_number: newPlate, reason: newReason}})
            }});
            const data = await res.json();
            if(data.error) setStatus("Error: " + data.error);
            else {{
                setStatus(`Added ${{newPlate}} successfully.`);
                setNewPlate('');
                setNewReason('');
                fetchBlacklist();
                setTimeout(() => setStatus(''), 3000);
            }}
        }} catch (e) {{ setStatus("Failed to add plate."); }}
        setIsSubmitting(false);
    }};

    const handleDelete = async (plate) => {{
        try {{
            const res = await fetch(`/api/v1/blacklist/${{plate}}`, {{ method: 'DELETE' }});
            if((await res.json()).status === 'success') {{
                fetchBlacklist();
            }}
        }} catch (e) {{ console.error("Failed to delete plate."); }}
    }};

    return (
        <div className="relative w-full h-screen overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900">
            
            {{/* BACKGROUND ACCENTS */}}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-200/40 rounded-full blur-[120px] pointer-events-none"></div>

            {{/* FLOATING TOP NAVIGATION BAR */}}
            <div className="absolute top-6 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex space-x-2">
                        <a href="/" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                        <a href="/tracking" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                        <a href="/blacklist" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Blacklist</a>
                        <a href="/geofence" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                        <a href="/chat" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                        <a href="/alerts" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    </div>
                </div>
            </div>

            {{/* MAIN CONTENT AREA */}}
            <div className="absolute top-28 left-6 right-6 bottom-6 flex gap-6 z-[900]">
                
                {{/* LEFT PANEL: ADD FORM */}}
                <div className="w-[450px] flex-shrink-0 rounded-3xl bg-gradient-to-br from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_20px_50px_rgba(0,0,0,0.1)]">
                    <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-[22px]">
                        <div className="mb-8">
                            <div className="flex items-center justify-between mb-1">
                                <h2 className="text-3xl font-black text-gray-900 tracking-tight">Blacklist</h2>
                                <div className="relative flex items-center justify-center w-8 h-8">
                                    <span className="absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-30 animate-ping"></span>
                                    <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.8)]"></span>
                                </div>
                            </div>
                            <p className="text-xs font-bold uppercase tracking-widest text-rose-400">Target Vehicle Entry</p>
                        </div>

                        <form onSubmit={{handleAdd}} className="space-y-5 flex-1 flex flex-col">
                            <div>
                                <label className="text-[10px] font-black text-gray-400 mb-2 block uppercase tracking-widest">Target License Plate</label>
                                <input type="text" placeholder="e.g. DL2CQ3150" 
                                       className="w-full bg-gray-50 border-2 border-gray-100 focus:border-indigo-500 focus:bg-white rounded-2xl px-5 py-4 text-sm font-bold text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400 uppercase" 
                                       value={{newPlate}} onChange={{e => setNewPlate(e.target.value.toUpperCase())}} required />
                            </div>
                            <div className="flex-1 flex flex-col">
                                <label className="text-[10px] font-black text-gray-400 mb-2 block uppercase tracking-widest">Reason / Wanted Status</label>
                                <textarea placeholder="e.g. Stolen Vehicle / Wanted for investigation" 
                                          className="w-full flex-1 bg-gray-50 border-2 border-gray-100 focus:border-indigo-500 focus:bg-white rounded-2xl px-5 py-4 text-sm font-medium text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400 resize-none" 
                                          value={{newReason}} onChange={{e => setNewReason(e.target.value)}} required></textarea>
                            </div>
                            
                            {{status && (
                                <div className="text-[10px] font-black uppercase tracking-widest text-emerald-600 bg-emerald-50 p-3 rounded-xl text-center border border-emerald-100 flex items-center justify-center">
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                    {{status}}
                                </div>
                            )}}

                            <button type="submit" disabled={{isSubmitting}} className="w-full bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 text-white py-4 rounded-2xl text-sm font-black uppercase tracking-wider shadow-xl shadow-indigo-500/30 transition-transform transform hover:-translate-y-1 flex justify-center items-center group mt-auto">
                                <svg className={{`w-5 h-5 mr-2 ${{isSubmitting ? 'animate-spin' : 'group-hover:scale-110 transition-transform'}}`}} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={{isSubmitting ? "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" : "M12 6v6m0 0v6m0-6h6m-6 0H6"}}></path></svg>
                                Add Target
                            </button>
                        </form>
                    </div>
                </div>
                
                {{/* RIGHT PANEL: WATCHLIST TABLE */}}
                <div className="flex-1 rounded-3xl bg-gradient-to-br from-indigo-500 via-cyan-400 to-fuchsia-500 p-[2px] shadow-[0_20px_50px_rgba(0,0,0,0.1)]">
                    <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-[22px]">
                        <h2 className="text-[10px] font-black text-gray-400 mb-6 uppercase tracking-widest border-b border-gray-100 pb-4 flex items-center">
                            <svg className="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                            Active Watchlist Directory
                        </h2>
                        
                        <div className="overflow-y-auto flex-1 pr-2 custom-scrollbar relative">
                            <table className="w-full text-sm text-left">
                                <thead className="text-[10px] text-gray-400 uppercase tracking-widest sticky top-0 bg-white/95 backdrop-blur-xl z-10">
                                    <tr>
                                        <th className="px-6 py-4 rounded-tl-xl">Target Plate</th>
                                        <th className="px-6 py-4">Wanted Reason</th>
                                        <th className="px-6 py-4">Registry Date</th>
                                        <th className="px-6 py-4 text-right rounded-tr-xl">Action</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-50">
                                    {{blacklist.length === 0 ? (
                                        <tr><td colSpan="4" className="px-6 py-12 text-center text-gray-400 font-bold italic bg-gray-50/50 rounded-xl">No active targets in network.</td></tr>
                                    ) : (
                                        blacklist.map((b, i) => (
                                            <tr key={{i}} className="hover:bg-gray-50/80 transition-colors group" style={{{{animation: `fade-in 0.4s ease-out ${{i * 0.05}}s both`}}}}>
                                                <td className="px-6 py-4 font-mono font-black text-gray-900 flex items-center">
                                                    <div className="w-2 h-2 rounded-full bg-rose-500 mr-3 shadow-[0_0_8px_rgba(244,63,94,0.6)]"></div>
                                                    {{b.plate_number}}
                                                </td>
                                                <td className="px-6 py-4 font-medium text-gray-600">{{b.reason}}</td>
                                                <td className="px-6 py-4 text-xs font-bold text-gray-400">{{new Date(b.created_at).toLocaleString(undefined, {{dateStyle: 'medium', timeStyle: 'short'}})}}</td>
                                                <td className="px-6 py-4 text-right">
                                                    <button onClick={{() => handleDelete(b.plate_number)}} className="text-gray-400 hover:text-rose-600 bg-white hover:bg-rose-50 px-4 py-2 rounded-lg text-xs font-black uppercase tracking-wider border-2 border-transparent hover:border-rose-100 shadow-sm transition-all transform hover:-translate-y-0.5">
                                                        Revoke
                                                    </button>
                                                </td>
                                            </tr>
                                        ))
                                    )}}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}}

class ErrorBoundary extends React.Component {{
    constructor(props) {{ super(props); this.state = {{ hasError: false, error: null }}; }}
    static getDerivedStateFromError(error) {{ return {{ hasError: true, error }}; }}
    render() {{ 
        if (this.state.hasError) return <div style={{{{color:'white', padding:'40px', background:'red'}}}}><h1>UI Crash!</h1><pre>{{this.state.error.toString()}}</pre></div>; 
        return this.props.children; 
    }}
}}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<ErrorBoundary><BlacklistApp /></ErrorBoundary>);
</script>
</body>
</html>"""

with open("blacklist.html", "w", encoding="utf-8") as f:
    f.write(blacklist_html)

print("Rewrote blacklist.html completely with the perfect advanced white UI.")
