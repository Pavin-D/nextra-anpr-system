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

export default function DatabaseApp() {
    const [tables, setTables] = React.useState([]);
    const [activeTable, setActiveTable] = React.useState(null);
    const [tableData, setTableData] = React.useState([]);
    const [loading, setLoading] = React.useState(true);
        const [showSidebar, setShowSidebar] = React.useState(true);
    const [deleteModal, setDeleteModal] = React.useState({ show: false, pkVal: null, table: null });
    const [deleteAllModal, setDeleteAllModal] = React.useState(false);

    React.useEffect(() => {
        fetchTables();
    }, []);

    const fetchTables = async () => {
        try {
            const res = await fetch('/api/v1/database/tables');
            const data = await res.json();
            setTables(data.tables ? data.tables.filter(t => t.name !== 'cameras') : []);
            if (data.tables && data.tables.length > 0 && !activeTable) {
                handleTableSelect(data.tables[0]);
            }
        } catch (e) {
            console.error('Error fetching tables');
        }
        setLoading(false);
    };

    const handleTableSelect = async (table) => {
        setActiveTable(table);
        setLoading(true);
        try {
            const res = await fetch(`/api/v1/database/data/${table.name}`);
            const data = await res.json();
            setTableData(data.rows || []);
        } catch (e) {
            console.error('Error fetching table data');
        }
        setLoading(false);
    };

        const handleDeleteAllRequest = () => { setDeleteAllModal(true); };
    const executeDeleteAll = async () => {
        try {
            const res = await fetch(`/api/v1/database/clear/${activeTable.name}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                handleTableSelect(activeTable);
                fetchTables();
                setDeleteAllModal(false);
            } else { alert("Failed to clear table: " + (data.error || "Unknown error")); }
        } catch (e) { console.error('Error clearing table', e); }
    };

    const handleDeleteRequest = (pkVal) => {
        setDeleteModal({ show: true, pkVal, table: activeTable.name });
    };

    const executeDelete = async () => {
        const { pkVal, table } = deleteModal;
        try {
            const res = await fetch(`/api/v1/database/data/${table}/${encodeURIComponent(pkVal)}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                handleTableSelect(activeTable);
                fetchTables();
                setDeleteModal({ show: false, pkVal: null, table: null });
            } else {
                alert("Failed to delete record: " + (data.error || "Unknown error"));
            }
        } catch (e) {
            console.error('Error deleting record', e);
        }
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
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex items-center space-x-1 lg:space-x-2 ml-auto">
                    <a href="/" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                    <a href="/tracking" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                    <a href="/blacklist" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                    <a href="/geofence" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                    <a href="/chat" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                    <a href="/alerts" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    <a href="/database" className="px-3 py-2 text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Database</a>
                    <a href="/videos" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Videos</a>
                    <button onClick={() => window.triggerLogout()} className="px-3 py-2 ml-2 flex items-center text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>
                </div>
                </div>
            </div>

            {/* MAIN CONTENT AREA */}
            <div className="absolute top-32 left-6 right-6 bottom-6 flex gap-6 z-[900]">
                
                {/* LEFT COLUMN: TABLES LIST */}
                <div className={`flex-shrink-0 h-full flex flex-col bg-white/60 backdrop-blur-md overflow-hidden transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? "w-64 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] rounded-[22px] opacity-100" : "w-0 border-0 opacity-0"}`}>
                    <div className="p-5 border-b border-gray-100 bg-white/90">
                        <h2 className="text-sm font-black text-gray-900 uppercase tracking-widest">Data Clusters</h2>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white/50">
                        {tables.map(table => (
                            <button key={table.name} onClick={() => handleTableSelect(table)} 
                                className={`w-full text-left px-4 py-3 rounded-xl border transition-all ${activeTable?.name === table.name ? 'bg-indigo-50 border-indigo-200 shadow-sm' : 'bg-white border-transparent hover:border-indigo-100 hover:shadow-sm'}`}>
                                <div className="text-xs font-black uppercase tracking-widest text-gray-800 mb-1">{table.name}</div>
                                <div className="text-[10px] font-bold text-indigo-500">{table.count} Records</div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* RIGHT COLUMN: DATA VIEWER */}
                <div className="flex-1 h-full flex flex-col bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md rounded-[22px] overflow-hidden">
                    {activeTable ? (
                        <div className="w-full h-full flex flex-col bg-white/90">
                            <div className="p-5 border-b border-gray-100 flex justify-between items-center bg-white/50">
                                <div>
                                    <h2 className="text-lg font-black text-gray-900 tracking-tight uppercase">Cluster: {activeTable.name}</h2>
                                    <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mt-1">Primary Key: {activeTable.pk}</p>
                                </div>
                                <div className="flex items-center space-x-3">
                                    {activeTable.name === 'plate_detections' && (
                                        <button onClick={handleDeleteAllRequest} className="px-4 py-2 bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700 text-white rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5 flex items-center">
                                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                            Delete All Data
                                        </button>
                                    )}
                                    <div className="text-[10px] font-black uppercase tracking-widest text-rose-500 bg-rose-50 px-3 py-2 rounded-xl border border-rose-100">
                                        Administrative Access Active
                                    </div>
                                </div>
                            </div>
                            
                            <div className="flex-1 overflow-auto custom-scrollbar p-0">
                                {loading ? (
                                    <div className="flex justify-center items-center h-40">
                                        <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
                                    </div>
                                ) : tableData.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                                        <p className="font-bold uppercase tracking-widest text-xs">Cluster is empty</p>
                                    </div>
                                ) : (
                                    <table className="w-full text-left border-collapse">
                                        <thead className="bg-gray-50/80 sticky top-0 backdrop-blur-md border-b border-gray-200 z-10">
                                            <tr>
                                                {Object.keys(tableData[0]).map(key => (
                                                    <th key={key} className="px-4 py-3 text-[10px] font-black uppercase tracking-widest text-gray-500 whitespace-nowrap">{key}</th>
                                                ))}
                                                <th className="px-4 py-3 text-[10px] font-black uppercase tracking-widest text-rose-500 text-right">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {tableData.map((row, i) => (
                                                <tr key={i} className="hover:bg-indigo-50/30 transition-colors animate-fade-in">
                                                    {Object.keys(row).map(key => (
                                                        <td key={key} className="px-4 py-3 text-xs font-medium text-gray-700 whitespace-nowrap max-w-[200px] overflow-hidden text-ellipsis" title={String(row[key])}>
                                                            {String(row[key])}
                                                        </td>
                                                    ))}
                                                    <td className="px-4 py-3 text-right">
                                                        {activeTable.name !== 'cameras' && (
                                                            <button onClick={() => handleDeleteRequest(row[activeTable.pk])} 
                                                                    className="text-[9px] font-black uppercase tracking-widest bg-white text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 px-3 py-1.5 rounded-lg transition-colors shadow-sm">
                                                                Delete
                                                            </button>
                                                        )}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                )}
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center bg-white/50 text-gray-400 text-xs font-bold uppercase tracking-widest">
                            Select a cluster to view records
                        </div>
                    )}
                </div>
            </div>
            {/* CUSTOM DELETE CONFIRMATION MODAL */}
            {deleteModal.show && (
                <div className="fixed inset-0 z-[10000] bg-slate-900/40 backdrop-blur-md flex items-center justify-center animate-fade-in">
                    <div className="bg-white/95 backdrop-blur-3xl border-2 border-rose-100 p-8 rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.2)] max-w-sm w-full mx-4 text-center transform scale-100 animate-fade-in">
                        <div className="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-rose-100 shadow-inner">
                            <svg className="w-8 h-8 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        </div>
                        <h2 className="text-2xl font-black text-gray-900 tracking-tight mb-2">Confirm Deletion</h2>
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2">Target Cluster: <span className="text-rose-500">{deleteModal.table}</span></p>
                        <p className="text-xs font-medium text-gray-600 mb-8">Are you sure you want to permanently delete record <span className="font-black text-gray-900">#{deleteModal.pkVal}</span>? This action cannot be undone.</p>
                        <div className="flex space-x-3">
                            <button onClick={() => setDeleteModal({ show: false, pkVal: null, table: null })} className="flex-1 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-gray-200 shadow-sm">Cancel</button>
                            <button onClick={executeDelete} className="flex-1 px-4 py-3 bg-gradient-to-r from-rose-500 to-red-500 hover:from-rose-600 hover:to-red-600 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5">Delete</button>
                        </div>
                    </div>
                </div>
            )}
            {deleteAllModal && (
                <div className="fixed inset-0 z-[10000] bg-slate-900/40 backdrop-blur-md flex items-center justify-center animate-fade-in">
                    <div className="bg-white/95 backdrop-blur-3xl border-2 border-rose-500 p-8 rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] max-w-sm w-full mx-4 text-center transform scale-100 animate-fade-in">
                        <div className="w-16 h-16 bg-rose-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg shadow-rose-500/30">
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        </div>
                        <h2 className="text-2xl font-black text-gray-900 tracking-tight mb-2">NUKE CLUSTER</h2>
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2">Target: <span className="text-rose-500">{activeTable?.name}</span></p>
                        <p className="text-xs font-medium text-gray-600 mb-8">Are you absolutely sure you want to annihilate ALL records in this cluster? This is irreversible.</p>
                        <div className="flex space-x-3">
                            <button onClick={() => setDeleteAllModal(false)} className="flex-1 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-gray-200 shadow-sm">Cancel</button>
                            <button onClick={executeDeleteAll} className="flex-1 px-4 py-3 bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5">Wipe Data</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}