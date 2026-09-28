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

function TrackingApp() {
    const [plateSearch, setPlateSearch] = React.useState('');
    const [status, setStatus] = React.useState('');
    const [knownPlates, setKnownPlates] = React.useState([]);
    const [isSearching, setIsSearching] = React.useState(false);
    const [showSidebar, setShowSidebar] = React.useState(true);
    
    const mapRef = React.useRef(null);
    const mapInstance = React.useRef(null);
    const trajectoryLayer = React.useRef(null);

    React.useEffect(() => {
        if (!mapInstance.current && mapRef.current) {
            mapInstance.current = L.map(mapRef.current, { zoomControl: false }).setView([28.6200, 77.2260], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(mapInstance.current);
            
            L.control.zoom({ position: 'bottomright' }).addTo(mapInstance.current);
            trajectoryLayer.current = L.layerGroup().addTo(mapInstance.current);
            setTimeout(() => { if (mapInstance.current) mapInstance.current.invalidateSize(); }, 500);
            
            const camIcon = L.icon({
                iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
            });
            
            L.marker([28.6315, 77.2167], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_01</b><br>Connaught Place North');
            L.marker([28.6258, 77.2343], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_02</b><br>Mandi House Circle');
            L.marker([28.6129, 77.2295], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_03</b><br>India Gate Roundabout');
        }
        
        setPlates([{ plate_number: 'KA02MN1828', last_seen: '2026-09-28 14:30', total_detections: 12 }, { plate_number: 'DL4CAB4421', last_seen: '2026-09-28 14:31', total_detections: 5 }]); setFilteredPlates([{ plate_number: 'KA02MN1828', last_seen: '2026-09-28 14:30', total_detections: 12 }, { plate_number: 'DL4CAB4421', last_seen: '2026-09-28 14:31', total_detections: 5 }]); setLoading(false); return;
            .then(r => r.json())
            .then(data => setKnownPlates(data.plates || []))
            .catch(e => console.error("Error fetching plates", e));
    }, []);

    const searchTrajectory = async (plateOverride) => {
        const plate = typeof plateOverride === 'string' ? plateOverride : plateSearch;
        if (!plate) return;
        setPlateSearch(plate.toUpperCase());
        trajectoryLayer.current.clearLayers();
        setStatus("Tracing optimal path...");
        setIsSearching(true);
        try {
            const res = await fetch(`/api/v1/trajectory/${plate.toUpperCase()}`);
            const data = await res.json();
            if (!data.trajectory || data.trajectory.length === 0) {
                setStatus(`No detections found for ${plate}`);
                setIsSearching(false);
                return;
            }
            const latlngs = data.trajectory.map(p => [p.lat, p.long]);
            
            if (latlngs.length > 1) {
                try {
                    const coords = data.trajectory.map(p => `${p.long},${p.lat}`).join(';');
                    const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson&alternatives=true`;
                    const osrmRes = await fetch(osrmUrl);
                    const osrmData = await osrmRes.json();
                    
                    if (osrmData.routes && osrmData.routes.length > 0) {
                        for (let i = osrmData.routes.length - 1; i >= 0; i--) {
                            const isOptimal = (i === 0);
                            L.geoJSON(osrmData.routes[i].geometry, {
                                style: { 
                                    color: isOptimal ? '#4f46e5' : '#94a3b8', 
                                    weight: isOptimal ? 6 : 4, 
                                    opacity: isOptimal ? 0.9 : 0.6,
                                    dashArray: isOptimal ? '' : '8, 8'
                                }
                            }).addTo(trajectoryLayer.current);
                        }
                    } else {
                        L.polyline(latlngs, {color: '#4f46e5', weight: 6, dashArray: '10, 15'}).addTo(trajectoryLayer.current);
                    }
                } catch (err) {
                    L.polyline(latlngs, {color: '#4f46e5', weight: 6, dashArray: '10, 15'}).addTo(trajectoryLayer.current);
                }
            }

            data.trajectory.forEach((p, index) => {
                L.circleMarker([p.lat, p.long], {color: '#ec4899', fillColor: '#ec4899', radius: 8, fillOpacity: 1})
                 .bindPopup(`<b>${p.location_name || 'Node'}</b><br/>Time: ${new Date(p.timestamp).toLocaleTimeString()}`)
                 .addTo(trajectoryLayer.current).openPopup();
            });
            mapInstance.current.fitBounds(trajectoryLayer.current.getBounds(), {padding: [100, 100]});
            setStatus(`Successfully mapped ${latlngs.length} nodes.`);
        } catch (e) { 
            setStatus(""); 
        }
        setIsSearching(false);
        if(window.innerWidth < 768) setShowSidebar(false);
    };

    return (
        <div className="relative w-full h-full overflow-hidden bg-gray-100 font-sans text-gray-900">
            
            {/* MAP BACKGROUND */}
            <div ref={mapRef} id="main-map" style={{position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, width: '100vw', height: '100vh', zIndex: 10}}></div>

            {/* FLOATING TOP NAVIGATION BAR */}
            <div className="absolute top-10 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.4)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <button onClick={() => setShowSidebar(!showSidebar)} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50/50">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                        </button>
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex items-center space-x-1 lg:space-x-2 ml-auto">
                    <a href="/" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                    <a href="/tracking" className="px-3 py-2 text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Tracking</a>
                    <a href="/blacklist" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                    <a href="/geofence" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                    <a href="/chat" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                    <a href="/alerts" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    <a href="/database" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Database</a>
                    <a href="/videos" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Videos</a>
                    <button onClick={() => window.triggerLogout()} className="px-3 py-2 ml-2 flex items-center text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>
                </div>
                </div>
            </div>
            
            {/* FLOATING SIDEBAR */}
            <div className={`absolute top-32 left-6 bottom-6 w-[400px] max-w-[90vw] z-[900] rounded-3xl bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md overflow-hidden p-0 transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] origin-left ${showSidebar ? 'translate-x-0 opacity-100 scale-100' : '-translate-x-[50px] opacity-0 scale-95 pointer-events-none'}`}>
                <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-none overflow-y-auto relative">
                    <div className="mb-8">
                        <div className="flex items-center justify-between mb-1">
                            <h2 className="text-3xl font-black text-gray-900 tracking-tight">Tracking</h2>
                            
                        </div>
                        <p className="text-xs font-bold uppercase tracking-widest text-indigo-400">Advanced Trajectory Map</p>
                    </div>
                    
                    {/* QUICK SEARCH */}
                    <div className="mb-8">
                        <div className="relative">
                            <input 
                                type="text" 
                                placeholder="Enter Target Plate (e.g. DL2CQ3150)" 
                                className="w-full bg-white border-2 border-transparent focus:border-indigo-500 rounded-2xl px-5 py-4 text-sm font-bold text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400 uppercase"
                                value={plateSearch} 
                                onChange={e => setPlateSearch(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && searchTrajectory()}
                            />
                            <button onClick={() => searchTrajectory()} className="absolute right-3 top-3 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 p-2 rounded-xl transition-colors">
                                <svg className={`w-5 h-5 ${isSearching ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                            </button>
                        </div>
                        {status && <p className="text-[10px] font-black uppercase tracking-widest text-indigo-600 mt-4 bg-indigo-50/50 p-2 rounded-xl text-center">{status}</p>}
                    </div>
                    
                    {/* DATABASE RECORDS */}
                    <div className="mb-8 flex-shrink-0">
                        <h2 className="text-[10px] font-black text-gray-400 mb-4 uppercase tracking-widest border-b border-gray-100 pb-2">Active Network Entities</h2>
                        <div className="grid grid-cols-2 gap-3">
                            {knownPlates.length === 0 ? (
                                <span className="text-xs text-gray-400 italic font-bold col-span-2">Awaiting telemetry...</span>
                            ) : (
                                knownPlates.map((p, i) => (
                                    <button 
                                        key={i} 
                                        onClick={() => searchTrajectory(p)}
                                        style={{ animation: `fade-in 0.4s ease-out ${i * 0.05}s both` }}
                                        className="relative group flex items-center justify-between px-3.5 py-3 bg-white border border-gray-100 hover:border-indigo-300 rounded-xl font-mono shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden">
                                        <div className="absolute inset-0 bg-gradient-to-r from-indigo-50/0 via-indigo-50/70 to-indigo-100/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 ease-in-out z-0"></div>
                                        
                                        <div className="flex items-center space-x-2.5 relative z-10">
                                            <div className="w-1.5 h-1.5 rounded-full bg-slate-300 group-hover:bg-indigo-500 group-hover:shadow-[0_0_8px_rgba(99,102,241,0.8)] transition-all duration-300"></div>
                                            <span className="text-xs font-black text-gray-700 group-hover:text-indigo-700 transition-colors">{p}</span>
                                        </div>
                                        
                                        <div className="relative z-10 bg-gray-50 group-hover:bg-indigo-100 p-1.5 rounded-md transition-colors shadow-sm">
                                            <svg className="w-3 h-3 text-gray-400 group-hover:text-indigo-600 transform group-hover:translate-x-0.5 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M9 5l7 7-7 7"></path></svg>
                                        </div>
                                    </button>
                                ))
                            )}
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




export default TrackingApp;
