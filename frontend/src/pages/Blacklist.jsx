import React, { useState, useEffect, useRef } from 'react';

const VoiceNav = () => {
            const [isActive, setIsActive] = React.useState(false);
            const [isProcessing, setIsProcessing] = React.useState(false);
            const activeRef = React.useRef(false);
            const recognitionRef = React.useRef(null);

            const toggleListening = () => {
                if (activeRef.current) {
                    activeRef.current = false;
                    setIsActive(false);
                    if(recognitionRef.current) recognitionRef.current.stop();
                    return;
                }

                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert("Voice Navigation is not supported in this browser.");
                    return;
                }

                activeRef.current = true;
                setIsActive(true);
                
                const recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onresult = (event) => {
                    const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
                    console.log("Heard:", transcript);
                    
                    const wakeWords = ["hey next", "hey extra", "a next", "hey nex", "an extra"];
                    const isWakeWord = wakeWords.some(w => transcript.includes(w));
                    
                    if (isWakeWord) {
                        setIsProcessing(true);
                        setTimeout(() => setIsProcessing(false), 2000);
                        
                        if (transcript.includes("dashboard") || transcript.includes("overview") || transcript.includes("home")) window.location.href = "/";
                        else if (transcript.includes("tracking") || transcript.includes("track")) window.location.href = "/tracking";
                        else if (transcript.includes("blacklist") || transcript.includes("black list")) window.location.href = "/blacklist";
                        else if (transcript.includes("geofence") || transcript.includes("geo fence")) window.location.href = "/geofence";
                        else if (transcript.includes("chat") || transcript.includes("search")) window.location.href = "/chat";
                    }
                };

                recognition.onend = () => {
                    if (activeRef.current) {
                        try { recognition.start(); } catch(e) {}
                    }
                };

                recognitionRef.current = recognition;
                recognition.start();
            };

            return (
                <div className="flex items-center space-x-3 ml-4">
                    <button onClick={toggleListening} title="Toggle Always-On Voice Assistant" 
                            className={`p-2 rounded-full border transition-all ${isActive ? 'bg-cyan-500/10 border-cyan-500 text-cyan-400 shadow-sm' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-950'}`}>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
                    </button>
                    {isActive && (
                        <span className={`text-[10px] font-bold uppercase tracking-widest ${isProcessing ? 'text-rose-500 animate-pulse' : 'text-cyan-400 animate-pulse'}`}>
                            {isProcessing ? 'Command Received' : 'Listening...'}
                        </span>
                    )}
                </div>
            );
        };

function BlacklistApp() {
    const [blacklist, setBlacklist] = React.useState([]);
    const [newPlate, setNewPlate] = React.useState('');
    const [newReason, setNewReason] = React.useState('');
    const [status, setStatus] = React.useState('');
    const [isSubmitting, setIsSubmitting] = React.useState(false);
    const [showSidebar, setShowSidebar] = React.useState(true);

    React.useEffect(() => {
        fetchBlacklist();
    }, []);

    const fetchBlacklist = async () => {
        try {
            const res = await fetch('/api/v1/blacklist');
            const data = await res.json();
            setBlacklist(data.blacklist || []);
        } catch (e) {
            console.error("Error fetching blacklist", e);
        }
    };

    const handleAdd = async (e) => {
        e.preventDefault();
        if(!newPlate || !newReason) return;
        setIsSubmitting(true);
        try {
            const res = await fetch('/api/v1/blacklist', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plate_number: newPlate, reason: newReason})
            });
            const data = await res.json();
            if(data.error) setStatus("Error: " + data.error);
            else {
                setStatus(`Added ${newPlate} successfully.`);
                setNewPlate('');
                setNewReason('');
                fetchBlacklist();
                setTimeout(() => setStatus(''), 3000);
            }
        } catch (e) { setStatus("Failed to add plate."); }
        setIsSubmitting(false);
    };

    const handleDelete = async (plate) => {
        try {
            const res = await fetch(`/api/v1/blacklist/${plate}`, { method: 'DELETE' });
            if((await res.json()).status === 'success') {
                fetchBlacklist();
            }
        } catch (e) { console.error("Failed to delete plate."); }
    };

    return (
        <div className="relative w-full h-full overflow-hidden bg-gradient-to-br from-gray-50 to-gray-200 font-sans text-gray-900">
            
            {/* BACKGROUND ACCENTS */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-200/40 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-200/40 rounded-full blur-[120px] pointer-events-none"></div>

            {/* FLOATING TOP NAVIGATION BAR */}
            <div className="absolute top-10 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.2)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <button onClick={() => setShowSidebar(!showSidebar)} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50/50 mr-4"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg></button>
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex items-center space-x-1 lg:space-x-2 ml-auto">
                    <a href="/" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                    <a href="/tracking" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                    <a href="/blacklist" className="px-3 py-2 text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Blacklist</a>
                    <a href="/geofence" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                    <a href="/chat" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                    <a href="/alerts" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    <a href="/database" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Database</a>
                    <a href="/videos" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Videos</a>
                    <button onClick={() => window.triggerLogout()} className="px-3 py-2 ml-2 flex items-center text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>
                </div>
                </div>
            </div>

            {/* MAIN CONTENT AREA */}
            <div className="absolute top-32 left-6 right-6 bottom-6 flex gap-6 z-[900]">
                
                {/* LEFT PANEL: ADD FORM */}
                <div className={`flex-shrink-0 bg-white/60 backdrop-blur-md overflow-hidden transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? "w-[450px] border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] rounded-3xl opacity-100" : "w-0 border-0 opacity-0"}`}>
                    <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-none">
                        <div className="mb-8">
                            <div className="flex items-center justify-between mb-1">
                                <h2 className="text-3xl font-black text-gray-900 tracking-tight">Blacklist</h2>
                                
                            </div>
                            <p className="text-xs font-bold uppercase tracking-widest text-rose-400">Target Vehicle Entry</p>
                        </div>

                        <form onSubmit={handleAdd} className="space-y-5 flex-1 flex flex-col">
                            <div>
                                <label className="text-[10px] font-black text-gray-400 mb-2 block uppercase tracking-widest">Target License Plate</label>
                                <input type="text" placeholder="e.g. DL2CQ3150" 
                                       className="w-full bg-gray-50 border-2 border-gray-100 focus:border-indigo-500 focus:bg-white rounded-2xl px-5 py-4 text-sm font-bold text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400 uppercase" 
                                       value={newPlate} onChange={e => setNewPlate(e.target.value.toUpperCase())} required />
                            </div>
                            <div className="flex-1 flex flex-col">
                                <label className="text-[10px] font-black text-gray-400 mb-2 block uppercase tracking-widest">Reason / Wanted Status</label>
                                <textarea placeholder="e.g. Stolen Vehicle / Wanted for investigation" 
                                          className="w-full flex-1 bg-gray-50 border-2 border-gray-100 focus:border-indigo-500 focus:bg-white rounded-2xl px-5 py-4 text-sm font-medium text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400 resize-none" 
                                          value={newReason} onChange={e => setNewReason(e.target.value)} required></textarea>
                            </div>
                            
                            {status && (
                                <div className="text-[10px] font-black uppercase tracking-widest text-emerald-600 bg-emerald-50 p-3 rounded-xl text-center border border-emerald-100 flex items-center justify-center">
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                    {status}
                                </div>
                            )}

                            <button type="submit" disabled={isSubmitting} className="w-full bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 text-white py-4 rounded-2xl text-sm font-black uppercase tracking-wider shadow-xl shadow-indigo-500/30 transition-transform transform hover:-translate-y-1 flex justify-center items-center group mt-auto">
                                <svg className={`w-5 h-5 mr-2 ${isSubmitting ? 'animate-spin' : 'group-hover:scale-110 transition-transform'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={isSubmitting ? "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" : "M12 6v6m0 0v6m0-6h6m-6 0H6"}></path></svg>
                                Add Target
                            </button>
                        </form>
                    </div>
                </div>
                
                {/* RIGHT PANEL: WATCHLIST TABLE */}
                <div className="flex-1 rounded-3xl bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md overflow-hidden p-0">
                    <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-none">
                        <h2 className="text-[10px] font-black text-gray-400 mb-6 uppercase tracking-widest border-b border-gray-100 pb-4 flex items-center">
                            <svg className="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                            Active Watchlist Directory
                        </h2>
                        
                        <div className="overflow-y-auto flex-1 pr-2 custom-scrollbar relative">
                            <table className="w-full text-sm text-left border-separate border-spacing-y-3">
                                <thead className="text-[10px] text-gray-400 uppercase tracking-widest sticky top-0 bg-white/95 backdrop-blur-xl z-20">
                                    <tr>
                                        <th className="px-6 py-2 font-black">Target Plate</th>
                                        <th className="px-6 py-2 font-black">Wanted Reason</th>
                                        <th className="px-6 py-2 font-black">Registry Date</th>
                                        <th className="px-6 py-2 text-right font-black">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {blacklist.length === 0 ? (
                                        <tr><td colSpan="4" className="px-6 py-12 text-center text-gray-400 font-bold italic bg-gray-50/80 rounded-2xl border-2 border-dashed border-gray-200">No active targets in network.</td></tr>
                                    ) : (
                                        blacklist.map((b, i) => (
                                            <tr key={i} className="bg-gray-50/50 hover:bg-white hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300 group rounded-2xl" style={{animation: `fade-in 0.4s ease-out ${i * 0.05}s both`}}>
                                                <td className="px-6 py-4 rounded-l-2xl border-y border-l border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <div className="inline-flex items-center px-4 py-1.5 bg-gray-900 border border-gray-700 rounded-lg shadow-inner group-hover:bg-gray-800 transition-colors">
                                                        
                                                        <span className="font-mono font-black text-cyan-400 tracking-wider text-sm">{b.plate_number}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 border-y border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <div className="flex items-start max-w-[250px]">
                                                        <svg className="w-4 h-4 text-rose-500 mr-2 mt-0.5 flex-shrink-0 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                                        <span className="font-bold text-gray-700 leading-snug group-hover:text-indigo-900 transition-colors">{b.reason}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 border-y border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <div className="inline-flex items-center text-xs font-black text-gray-500 bg-gray-100 px-3 py-1.5 rounded-md border border-gray-200 group-hover:bg-indigo-50 group-hover:border-indigo-100 group-hover:text-indigo-600 transition-colors">
                                                        <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                                        {new Date(b.created_at).toLocaleString(undefined, {dateStyle: 'medium', timeStyle: 'short'})}
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 text-right rounded-r-2xl border-y border-r border-gray-100 group-hover:border-indigo-100 transition-colors">
                                                    <button onClick={() => handleDelete(b.plate_number)} className="relative overflow-hidden inline-flex items-center justify-center bg-white border-2 border-gray-100 group-hover:border-rose-200 hover:!bg-rose-50 hover:!border-rose-300 text-gray-400 hover:!text-rose-600 px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-0.5">
                                                        <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                                        Revoke
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
        </div>
    );
}

class ErrorBoundary extends React.Component {
    constructor(props) { super(props); this.state = { hasError: false, error: null }; }
    static getDerivedStateFromError(error) { return { hasError: true, error }; }
    render() { 
        if (this.state.hasError) return <div style={{color:'white', padding:'40px', background:'red'}}><h1>UI Crash!</h1><pre>{this.state.error.toString()}</pre></div>; 
        return this.props.children; 
    }
}




export default BlacklistApp;
