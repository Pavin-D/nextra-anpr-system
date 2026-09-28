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

const CAMERAS = [
    {id: 'CAM_01', lat: 28.6315, lng: 77.2167},
    {id: 'CAM_02', lat: 28.6258, lng: 77.2343},
    {id: 'CAM_03', lat: 28.6129, lng: 77.2295}
];

function GeofenceApp() {
    const [detections, setDetections] = React.useState([]);
    const [status, setStatus] = React.useState('Draw a geofence on the map to scan area.');
    const [activeCameras, setActiveCameras] = React.useState([]);
    const [showSidebar, setShowSidebar] = React.useState(true);
    const [isScanning, setIsScanning] = React.useState(false);

    const mapRef = React.useRef(null);
    const mapInstance = React.useRef(null);
    const drawnItems = React.useRef(null);
    const trajectoryLayer = React.useRef(null);

    React.useEffect(() => {
        if (!mapInstance.current && mapRef.current) {
            mapInstance.current = L.map(mapRef.current, { zoomControl: false }).setView([28.6200, 77.2260], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap'
            }).addTo(mapInstance.current);
            
            L.control.zoom({ position: 'bottomright' }).addTo(mapInstance.current);
            setTimeout(() => { if (mapInstance.current) mapInstance.current.invalidateSize(); }, 500);

            // Add fixed cameras
            const camIcon = L.icon({
                iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                iconSize: [25, 41], iconAnchor: [12, 41]
            });
            
            CAMERAS.forEach(cam => {
                L.marker([cam.lat, cam.lng], {icon: camIcon})
                 .addTo(mapInstance.current)
                 .bindTooltip(`<b>${cam.id}</b>`, {permanent: true, direction: 'top', offset: [0,-40], className: 'font-mono text-[10px] font-black tracking-widest bg-indigo-600 text-white border-0 shadow-lg px-2 py-1 rounded'});
            });

            // Initialize Draw Feature
            trajectoryLayer.current = L.layerGroup().addTo(mapInstance.current);
            drawnItems.current = new L.FeatureGroup();
            mapInstance.current.addLayer(drawnItems.current);
            
            const drawControl = new L.Control.Draw({
                position: 'topright',
                edit: { featureGroup: drawnItems.current, remove: true },
                draw: {
                    polygon: { shapeOptions: { color: '#b91c1c', weight: 4, fillOpacity: 0.2, dashArray: '10, 10' } },
                    rectangle: { shapeOptions: { color: '#b91c1c', weight: 4, fillOpacity: 0.2, dashArray: '10, 10' } },
                    circle: { shapeOptions: { color: '#b91c1c', weight: 4, fillOpacity: 0.2, dashArray: '10, 10' } },
                    polyline: false, marker: false, circlemarker: false
                }
            });
            mapInstance.current.addControl(drawControl);

            mapInstance.current.on(L.Draw.Event.CREATED, function (e) {
                const layer = e.layer;
                drawnItems.current.addLayer(layer);
                analyzeAllGeofences();
            });
            
            mapInstance.current.on(L.Draw.Event.DELETED, function (e) {
                analyzeAllGeofences();
            });
            
            mapInstance.current.on(L.Draw.Event.EDITED, function (e) {
                analyzeAllGeofences();
            });
        }
    }, []);

    const analyzeAllGeofences = async () => {
        setIsScanning(true);
        setStatus('Analyzing restricted areas...');
        
        const insideCameras = new Set();
        
        drawnItems.current.eachLayer(layer => {
            let polyGeoJson;
            if (layer instanceof L.Circle) {
                const center = [layer.getLatLng().lng, layer.getLatLng().lat];
                const radius = layer.getRadius() / 1000;
                polyGeoJson = turf.circle(center, radius, {steps: 64, units: 'kilometers'});
            } else {
                polyGeoJson = layer.toGeoJSON();
            }

            CAMERAS.forEach(cam => {
                const pt = turf.point([cam.lng, cam.lat]);
                if (turf.booleanPointInPolygon(pt, polyGeoJson)) {
                    insideCameras.add(cam.id);
                }
            });
        });

        const cameraArray = Array.from(insideCameras);
        setActiveCameras(cameraArray);

        if (cameraArray.length === 0) {
            setStatus('No cameras detected in marked zones.');
            setDetections([]);
            setIsScanning(false);
            return;
        }

        setStatus(`Querying nodes: ${cameraArray.join(', ')}`);
        
        try {
            const res = await fetch('/api/v1/geofence-search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({cameras: cameraArray})
            });
            const data = await res.json();
            setDetections(data.detections || []);
            setStatus(`Identified ${data.detections.length} vehicles.`);
        } catch (e) {
            setStatus('Error establishing node uplink.');
            setDetections([]);
        }
        setIsScanning(false);
    };


    const viewVehicle = async (plate) => {
        setStatus(`Fetching telemetry map for ${plate}...`);
        trajectoryLayer.current.clearLayers();
        try {
            const res = await fetch(`/api/v1/trajectory/${plate}`);
            const data = await res.json();
            if (!data.trajectory || data.trajectory.length === 0) {
                setStatus(`No mapping data for ${plate}`);
                return;
            }
            const latlngs = data.trajectory.map(p => [p.lat, p.long]);
            if (latlngs.length > 1) {
                try {
                    const coords = data.trajectory.map(p => `${p.long},${p.lat}`).join(';');
                    const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson`;
                    const osrmRes = await fetch(osrmUrl);
                    const osrmData = await osrmRes.json();
                    if (osrmData.routes && osrmData.routes.length > 0) {
                        L.geoJSON(osrmData.routes[0].geometry, {
                            style: { color: '#4f46e5', weight: 6, opacity: 0.9 }
                        }).addTo(trajectoryLayer.current);
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
            setStatus(`Trajectory loaded for ${plate}.`);
        } catch(e) {
            setStatus("");
        }
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
                    <a href="/tracking" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                    <a href="/blacklist" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                    <a href="/geofence" className="px-3 py-2 text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Geofence</a>
                    <a href="/chat" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                    <a href="/alerts" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    <a href="/database" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Database</a>
                    <a href="/videos" className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider whitespace-nowrap rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Videos</a>
                    <button onClick={() => window.triggerLogout()} className="px-3 py-2 ml-2 flex items-center text-[11px] font-black uppercase tracking-wider whitespace-nowrap rounded-xl bg-rose-50 text-rose-500 hover:text-white border border-rose-200 hover:bg-rose-500 hover:border-rose-500 transition-all shadow-sm"><svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>Logout</button>
                </div>
                </div>
            </div>
            
            {/* FLOATING SIDEBAR */}
            <div className={`absolute top-32 left-6 bottom-6 w-[450px] max-w-[90vw] z-[900] rounded-3xl bg-white/60 border-2 border-indigo-200/80 shadow-[0_0_20px_rgba(99,102,241,0.15)] backdrop-blur-md overflow-hidden p-0 transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] origin-left ${showSidebar ? 'translate-x-0 opacity-100 scale-100' : '-translate-x-[50px] opacity-0 scale-95 pointer-events-none'}`}>
                <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-none overflow-hidden relative">
                    <div className="flex-shrink-0 mb-6">
                        <div className="flex items-center justify-between mb-1">
                            <h2 className="text-3xl font-black text-gray-900 tracking-tight">Geofence</h2>
                            
                        </div>
                        <p className="text-xs font-bold uppercase tracking-widest text-rose-400">Spatial Analytics Engine</p>
                    </div>
                    
                    {/* STATUS INDICATOR */}
                    <div className="flex-shrink-0 mb-6">
                        <div className="bg-gray-50 rounded-2xl p-4 border border-gray-100 flex items-center justify-between">
                            <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Scanner Status</span>
                            <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-md border ${isScanning ? 'bg-indigo-50 text-indigo-600 border-indigo-200' : 'bg-white text-gray-400 border-gray-200'}`}>
                                {status}
                            </span>
                        </div>
                    </div>

                    {/* ACTIVE NODES */}
                    <div className="flex-shrink-0 mb-6">
                        <h2 className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest border-b border-gray-100 pb-2">Engaged Nodes</h2>
                        <div className="flex flex-wrap gap-2">
                            {activeCameras.length === 0 ? (
                                <span className="text-xs text-gray-400 italic font-bold">Draw zone to engage nodes.</span>
                            ) : (
                                activeCameras.map((cam, i) => (
                                    <div key={i} className="px-3 py-1.5 bg-indigo-50 border border-indigo-100 text-indigo-700 text-[10px] rounded-lg font-mono font-black shadow-sm flex items-center" style={{animation: `fade-in 0.3s ease-out ${i * 0.05}s both`}}>
                                        
                                        {cam}
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                    
                    {/* DETECTIONS TABLE */}
                    <div className="flex-1 flex flex-col min-h-0">
                        <h2 className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest border-b border-gray-100 pb-2 flex-shrink-0">Zone Detections ({detections.length})</h2>
                        <div className="overflow-y-auto custom-scrollbar flex-1 pr-2 relative">
                            <div className="grid grid-cols-2 gap-3 pb-4">
                                {detections.length === 0 ? (
                                    <div className="col-span-2 px-4 py-8 text-center text-gray-400 font-bold italic bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center">
                                        <svg className="w-8 h-8 mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                        No telemetry captured
                                    </div>
                                ) : (
                                    detections.map((d, i) => (
                                        <div key={i} className="bg-white border border-gray-100 rounded-xl p-3 shadow-sm hover:shadow-md hover:border-indigo-200 transition-all duration-300 group flex flex-col justify-between transform hover:-translate-y-0.5" style={{animation: `fade-in 0.4s ease-out ${i * 0.05}s both`}}>
                                            <div className="flex justify-between items-start mb-3">
                                                <div className="font-mono font-black text-indigo-600 tracking-wider text-xs">
                                                    {d.plate_number}
                                                </div>
                                                <div className="text-[9px] font-black text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded flex items-center shadow-inner group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                                                    <svg className="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                    {d.camera_id}
                                                </div>
                                            </div>
                                            <div className="flex justify-between items-end border-t border-gray-50 pt-2 mt-auto mb-2">
                                                <div className="text-[9px] font-bold text-gray-400 uppercase tracking-widest">
                                                    {new Date(d.timestamp).toLocaleDateString(undefined, {dateStyle: 'short'})}
                                                </div>
                                                <div className="text-[10px] font-black text-gray-700 group-hover:text-indigo-900 transition-colors">
                                                    {new Date(d.timestamp).toLocaleTimeString(undefined, {timeStyle: 'short'})}
                                                </div>
                                            </div>
                                            <button onClick={() => viewVehicle(d.plate_number)} className="w-full mt-auto bg-gray-50 hover:bg-indigo-50 border border-gray-100 hover:border-indigo-100 text-gray-600 hover:text-indigo-600 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest transition-colors flex items-center justify-center">
                                                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                                                View Map Data
                                            </button>
                                        </div>
                                    ))
                                )}
                            </div>
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




export default GeofenceApp;
