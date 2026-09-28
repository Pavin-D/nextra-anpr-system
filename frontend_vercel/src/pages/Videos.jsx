import React, { useState, useEffect } from 'react';

export default function Videos() {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showSidebar, setShowSidebar] = useState(true);
    const [activeVideos, setActiveVideos] = useState([]); // Now an array for split screen
    const [isSplitScreen, setIsSplitScreen] = useState(false);
    const [deleteModal, setDeleteModal] = useState({ show: false, filename: null });

    useEffect(() => {
        fetchVideos();
    }, []);

    const fetchVideos = async () => {
    setVideos(["CAM_01_morning_traffic.mp4", "CAM_02_highway_accident.mp4", "CAM_03_city_center.mp4"]);
    setLoading(false);
};

    const handleDeleteRequest = (filename) => {
        setDeleteModal({ show: true, filename });
    };

    const executeDelete = async () => {
        try {
            const res = await fetch(`/api/v1/videos/delete/${encodeURIComponent(deleteModal.filename)}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) {
                setActiveVideos(activeVideos.filter(v => v !== deleteModal.filename));
                fetchVideos();
                setDeleteModal({ show: false, filename: null });
            } else {
                alert("Failed to delete video");
            }
        } catch (e) {
            console.error(e);
        }
    };

    const handleVideoSelect = (filename) => {
        if (isSplitScreen) {
            if (activeVideos.includes(filename)) {
                setActiveVideos(activeVideos.filter(v => v !== filename));
            } else {
                if (activeVideos.length < 4) {
                    setActiveVideos([...activeVideos, filename]);
                } else {
                    alert("Maximum 4 cameras in split screen mode.");
                }
            }
        } else {
            setActiveVideos([filename]);
        }
    };

    return (
        <div className="relative w-full h-full overflow-hidden bg-gray-50 font-sans text-gray-900">
            {/* FLOATING TOP NAVIGATION BAR */}
            <div className="absolute top-10 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.4)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                <div className="flex items-center space-x-4">
                    <button onClick={() => setShowSidebar(!showSidebar)} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50/50">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                    </button>
                    <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                </div>
                <div className="hidden md:flex items-center space-x-1 lg:space-x-2 ml-auto">
                    <a href="/" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                    <a href="/tracking" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                    <a href="/blacklist" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                    <a href="/geofence" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                    <a href="/chat" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                    <a href="/alerts" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    <a href="/database" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Database</a>
                    <a href="/videos" className="px-3 py-2 text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Videos</a>
                    <button onClick={() => window.triggerLogout()} className="px-3 py-2 ml-2 flex items-center text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>
                </div>
            </div>
            </div>

            {/* MAIN CONTENT AREA */}
            <div className="absolute top-32 left-6 right-6 bottom-6 flex gap-6 z-[900]">
                
                {/* LEFT COLUMN: VIDEOS LIST */}
                <div className={`flex-shrink-0 h-full flex flex-col bg-white/60 backdrop-blur-md overflow-hidden transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? "w-80 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] rounded-[22px] opacity-100" : "w-0 border-0 opacity-0"}`}>
                    <div className="p-5 border-b border-gray-100 bg-white/90">
                        <h2 className="text-sm font-black text-gray-900 uppercase tracking-widest">Video Archive</h2>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white/50 custom-scrollbar">
                        {loading ? (
                            <div className="text-center text-gray-400 text-xs font-bold uppercase tracking-widest mt-10">Loading...</div>
                        ) : videos.length === 0 ? (
                            <div className="text-center text-gray-400 text-xs font-bold uppercase tracking-widest mt-10">No Videos Found</div>
                        ) : videos.map(vid => {
                            const isSelected = activeVideos.includes(vid.filename);
                            return (
                                <div key={vid.filename} className={`w-full text-left p-4 rounded-xl border transition-all shadow-sm group ${isSelected ? 'bg-indigo-50 border-indigo-300' : 'bg-white border-transparent hover:border-indigo-100'}`}>
                                    <div className="flex justify-between items-start mb-2">
                                        <div className="text-xs font-black uppercase tracking-widest text-gray-800 break-all">{vid.filename}</div>
                                        <button onClick={(e) => { e.stopPropagation(); handleDeleteRequest(vid.filename); }} className="text-rose-400 hover:text-rose-600 transition-colors ml-2 flex-shrink-0">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                        </button>
                                    </div>
                                    <div className="text-[10px] font-bold text-gray-400 mb-3">{vid.size} • {new Date(vid.date).toLocaleString()}</div>
                                    <button onClick={() => handleVideoSelect(vid.filename)} className={`w-full py-2 rounded-lg font-bold text-[10px] uppercase tracking-widest transition-colors ${isSelected ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/30' : 'bg-indigo-50 hover:bg-indigo-100 text-indigo-600'}`}>
                                        {isSelected ? 'Selected' : (isSplitScreen ? '+ Add to Grid' : 'Watch Video')}
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* RIGHT COLUMN: VIDEO PLAYER */}
                <div className="flex-1 h-full rounded-[22px] border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] bg-white/60 backdrop-blur-md overflow-hidden relative transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] flex flex-col min-h-0">
                    <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-white/90 z-10 flex-shrink-0 h-16">
                        <div>
                            <h2 className="text-lg font-black text-gray-900 tracking-tight uppercase">
                                {activeVideos.length === 0 ? 'Media Player' : `Monitoring ${activeVideos.length} Feed(s)`}
                            </h2>
                        </div>
                        <div className="flex items-center">
                            <label className="flex items-center cursor-pointer mr-4">
                                <div className="relative">
                                    <input type="checkbox" className="sr-only" checked={isSplitScreen} onChange={() => {
                                        setIsSplitScreen(!isSplitScreen);
                                        if (activeVideos.length > 1 && !(!isSplitScreen)) {
                                            setActiveVideos([activeVideos[0]]);
                                        }
                                    }} />
                                    <div className={`block w-10 h-6 rounded-full transition-colors ${isSplitScreen ? 'bg-indigo-500' : 'bg-gray-300'}`}></div>
                                    <div className={`dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${isSplitScreen ? 'transform translate-x-4' : ''}`}></div>
                                </div>
                                <div className="ml-3 text-[10px] font-black text-gray-600 uppercase tracking-widest">
                                    Split Screen Mode
                                </div>
                            </label>
                        </div>
                    </div>
                    
                    {/* VIDEO GRID (CRITICAL LAYOUT FIX) */}
                    <div className="flex-1 p-4 bg-gray-900 min-h-0 relative overflow-hidden">
                        {activeVideos.length === 0 ? (
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500 bg-gray-50">
                                <svg className="w-16 h-16 mb-4 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                <p className="font-bold uppercase tracking-widest text-xs">Select a video to begin playback</p>
                            </div>
                        ) : (
                            <div className={`w-full h-full grid gap-4 ${
                                activeVideos.length === 1 ? 'grid-cols-1 grid-rows-1' :
                                activeVideos.length === 2 ? 'grid-cols-2 grid-rows-1' :
                                'grid-cols-2 grid-rows-2'
                            }`}>
                                {activeVideos.map(vid => (
                                    <div key={vid} className="relative w-full h-full bg-black rounded-xl overflow-hidden border border-gray-700 shadow-2xl flex items-center justify-center group">
                                        <video controls autoPlay loop className="w-full h-full object-contain">
                                            <source src={`/api/v1/videos/play/${vid}`} type="video/mp4" />
                                        </video>
                                        <div className="absolute top-3 left-3 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-lg shadow-lg text-[10px] text-white font-mono font-bold flex items-center tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                                            <svg className="w-3 h-3 text-red-500 mr-2 animate-pulse" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle></svg>
                                            {vid}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* DELETE MODAL */}
            {deleteModal.show && (
                <div className="fixed inset-0 z-[10000] bg-slate-900/60 backdrop-blur-md flex items-center justify-center animate-fade-in">
                    <div className="bg-white/95 backdrop-blur-3xl border-2 border-rose-100 p-8 rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] max-w-sm w-full mx-4 text-center transform scale-100 animate-fade-in">
                        <div className="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-rose-100 shadow-inner">
                            <svg className="w-8 h-8 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                        </div>
                        <h2 className="text-2xl font-black text-gray-900 tracking-tight mb-2">Delete Video</h2>
                        <p className="text-xs font-medium text-gray-600 mb-8">Are you sure you want to permanently delete <span className="font-black text-gray-900">{deleteModal.filename}</span>?</p>
                        <div className="flex space-x-3">
                            <button onClick={() => setDeleteModal({ show: false, filename: null })} className="flex-1 px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all border border-gray-200 shadow-sm">Cancel</button>
                            <button onClick={executeDelete} className="flex-1 px-4 py-3 bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700 text-white text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5">Delete</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

