

        
        
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
function Dashboard() {
            const [plateSearch, setPlateSearch] = React.useState('');
            const [status, setStatus] = React.useState('');
            const [alerts, setAlerts] = React.useState([]);
            
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

            const [telemetry, setTelemetry] = React.useState({success_rate: 0, cameras: []});
            const [bottlenecks, setBottlenecks] = React.useState([]);
            
            // Live AI Preview states
            const [showLivePreview, setShowLivePreview] = React.useState(false);
            const [aiProgress, setAiProgress] = React.useState(0);
            const [liveImgUrl, setLiveImgUrl] = React.useState('');
            
            const [showSidebar, setShowSidebar] = React.useState(true);
            const mapRef = React.useRef(null);
            const mapInstance = React.useRef(null);
            const trajectoryLayer = React.useRef(null);
            const heatLayer = React.useRef(null);
            const [files, setFiles] = React.useState({cam1: null, cam2: null, cam3: null});

            React.useEffect(() => {
                if (!mapInstance.current && mapRef.current) {
                    mapInstance.current = L.map(mapRef.current, { zoomControl: false }).setView([28.6200, 77.2260], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; OpenStreetMap &copy; CARTO'
                    }).addTo(mapInstance.current);
                    
                    L.control.zoom({ position: 'bottomright' }).addTo(mapInstance.current);
                    setTimeout(() => { if (mapInstance.current) mapInstance.current.invalidateSize(); }, 500);
                }
                    // Fix 3 predefined camera nodes on the map permanently
                    const camIcon = L.icon({
                        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
                    });
                    
                    L.marker([28.6315, 77.2167], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_01</b><br>Connaught Place North');
                    L.marker([28.6258, 77.2343], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_02</b><br>Mandi House Circle');
                    L.marker([28.6129, 77.2295], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_03</b><br>India Gate Roundabout');


                const fetchTelemetry = async () => {
                    try {
                        const res = await fetch('/api/v1/telemetry');
                        const data = await res.json();
                        setTelemetry({
                            success_rate: data.success_rate || 0,
                            cameras: data.cameras || []
                        });
                        if (data.alerts) setAlerts(data.alerts);

                        // Heatmap logic
                        const heatRes = await fetch('/api/v1/analytics/heatmap');
                        const heatData = await heatRes.json();
                        if (heatLayer.current) mapInstance.current.removeLayer(heatLayer.current);
                        if (heatData.heatmap) {
                            const heatPoints = heatData.heatmap.map(c => [c.lat, c.long, c.detection_count * 10]);
                            heatLayer.current = L.heatLayer(heatPoints, {radius: 40, blur: 20}).addTo(mapInstance.current);
                        }

} catch(e) { console.error(e); }
                };

                const fetchLiveProgress = async () => {
                    try {
                        const res = await fetch('/api/v1/progress');
                        const data = await res.json();
                        setAiProgress(data.progress);
                        if (data.latest_img) setLiveImgUrl('data:image/jpeg;base64,' + data.latest_img);
                    } catch (e) {}
                };

                fetchTelemetry();
                const interval = setInterval(fetchTelemetry, 5000);
                const liveInterval = setInterval(fetchLiveProgress, 1000);
                return () => { 
                    clearInterval(interval); 
                    clearInterval(liveInterval); 
                    if (mapInstance.current) { mapInstance.current.remove(); mapInstance.current = null; }
                };
            }, []);

            const handleSearch = async (e) => {
                if(e.key === 'Enter') {
                    setStatus(`Tracking ${plateSearch}...`);
                    try {
                        const res = await fetch(`/api/v1/trajectory?plate=${plateSearch}`);
                        const data = await res.json();
                        if (trajectoryLayer.current) mapInstance.current.removeLayer(trajectoryLayer.current);
                        
                        if (!data.trajectory || data.trajectory.length === 0) {
                            setStatus("No trajectory found.");
                            return;
                        }

                        const latlngs = data.trajectory.map(p => [p.lat, p.lng]);
                        trajectoryLayer.current = L.polyline(latlngs, {color: '#4f46e5', weight: 5, opacity: 0.8, dashArray: '10, 10'}).addTo(mapInstance.current);
                        mapInstance.current.fitBounds(trajectoryLayer.current.getBounds());
                        
                        latlngs.forEach((ll, i) => {
                            L.circleMarker(ll, {radius: 6, color: '#ec4899', fillColor: '#ec4899', fillOpacity: 1}).addTo(mapInstance.current)
                             .bindTooltip(data.trajectory[i].timestamp);
                        });
                        
                        setStatus(`Found ${latlngs.length} nodes.`);
                        setShowSidebar(false);
                    } catch (e) { setStatus("Error loading trajectory."); }
                }
            };

            const handleUpload = async () => {
                setStatus("Uploading feeds to multi-pipeline...");
                setShowLivePreview(true);
                setShowSidebar(false);
                const formData = new FormData();
                if(files.cam1) formData.append("cam1", files.cam1);
                if(files.cam2) formData.append("cam2", files.cam2);
                if(files.cam3) formData.append("cam3", files.cam3);
                
                try {
                    const res = await fetch('/api/v1/upload-feeds', { method: 'POST', body: formData });
                    setStatus(`SUCCESS: ${(await res.json()).message}`);
                } catch(e) { setStatus("Upload failed."); }
            };

            return (
                <div className="relative w-full h-screen overflow-hidden bg-gray-100 font-sans text-gray-900">
                    
                    {/* MAP BACKGROUND */}
                    <div ref={mapRef} id="main-map" style={{position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, width: '100vw', height: '100vh', zIndex: 10}}></div>

                    {/* TOAST NOTIFICATION */}
                    {toastAlert && (
                        <div className="absolute top-28 left-1/2 transform -translate-x-1/2 z-[9999] bg-white rounded-3xl shadow-[0_20px_50px_rgba(244,63,94,0.3)] border border-rose-100 overflow-hidden flex animate-bounce flex-col w-[450px]">
                            <div className="bg-gradient-to-r from-rose-500 to-red-500 text-white px-5 py-3 font-black tracking-widest text-sm flex items-center justify-between">
                                <div className="flex items-center">
                                    <span className="w-2.5 h-2.5 bg-white rounded-full animate-ping mr-3 shadow-lg"></span>
                                    CRITICAL THREAT DETECTED
                                </div>
                                <button onClick={() => setToastAlert(null)} className="text-white/80 hover:text-white transition-colors">&times;</button>
                            </div>
                            <div className="p-6 flex bg-white/95 backdrop-blur">
                                <div className="mr-5 text-rose-500">
                                    <svg className="w-12 h-12 drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                </div>
                                <div>
                                    <div className="text-2xl font-black text-gray-900 font-mono tracking-widest mb-1">{toastAlert.plate_number}</div>
                                    <div className="text-xs font-bold text-rose-600 mb-2 uppercase tracking-widest bg-rose-50 inline-block px-2 py-1 rounded-md">{toastAlert.alert_type}</div>
                                    <div className="text-xs font-medium text-gray-500 mb-3">{toastAlert.description}</div>
                                    <div className="inline-flex items-center bg-gray-50 border border-gray-100 text-gray-600 text-xs font-bold px-3 py-1.5 rounded-lg shadow-sm">
                                        <svg className="w-4 h-4 mr-1 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                                        {toastAlert.camera_id} &nbsp;|&nbsp; {new Date(toastAlert.timestamp).toLocaleTimeString()}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    {/* FLOATING TOP NAVIGATION BAR */}
                    <div className="absolute top-6 left-6 right-6 h-16 bg-white/80 backdrop-blur-2xl border border-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.08)] flex items-center px-6 justify-between z-[1000] transition-all">
                        <div className="flex items-center space-x-4">
                            <button onClick={() => setShowSidebar(!showSidebar)} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50/50">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                            </button>
                            <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                            <VoiceNav />
                        </div>
                        <div className="hidden md:flex space-x-2">
                            <a href="/" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Dashboard</a>
                            <a href="/tracking" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                            <a href="/blacklist" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                            <a href="/geofence" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                            <a href="/chat" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                            <a href="/alerts" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                        </div>
                    </div>

                    {/* LIVE AI PREVIEW MODAL */}
                    {showLivePreview && (
                        <div className="absolute top-28 right-6 w-96 bg-white/90 backdrop-blur-2xl border border-white rounded-3xl shadow-[0_30px_60px_rgba(0,0,0,0.15)] overflow-hidden z-[999] transition-all">
                            <div className="bg-gradient-to-r from-indigo-600 to-blue-500 px-5 py-3 flex justify-between items-center shadow-inner">
                                <h3 className="font-bold text-xs text-white tracking-widest uppercase">Live AI Engine</h3>
                                <button onClick={() => setShowLivePreview(false)} className="text-white/80 hover:text-white font-bold text-lg leading-none">&times;</button>
                            </div>
                            <div className="p-4 relative">
                                <div className="rounded-2xl overflow-hidden shadow-inner border border-gray-100 bg-gray-50 relative">
                                    <img src={liveImgUrl} alt="AI Stream" className="w-full h-auto min-h-[200px] object-cover mix-blend-multiply" onError={(e) => e.target.src=''} />
                                    <div className="absolute top-3 left-3 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-lg shadow-lg text-[10px] text-emerald-400 font-mono font-bold flex items-center uppercase tracking-widest">
                                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span>YOLOv11 Active
                                    </div>
                                </div>
                            </div>
                            <div className="px-5 pb-5 pt-2">
                                <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-2">
                                    <span>Processing Feeds</span>
                                    <span className="text-indigo-600">{aiProgress}%</span>
                                </div>
                                <div className="w-full bg-gray-100 rounded-full h-2 shadow-inner overflow-hidden">
                                    <div className="bg-gradient-to-r from-indigo-500 to-blue-500 h-2 rounded-full transition-all duration-300 ease-out" style={{width: `${aiProgress}%`}}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    {/* FLOATING SIDEBAR */}
                    <div className={`absolute top-28 left-6 bottom-6 w-[400px] max-w-[90vw] bg-white/80 backdrop-blur-3xl p-8 flex flex-col shadow-[0_20px_50px_rgba(0,0,0,0.1)] rounded-3xl border border-white z-[900] overflow-y-auto transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${showSidebar ? 'translate-x-0' : '-translate-x-[120%]'}`}>
                        <div className="mb-8">
                            <div className="flex items-center justify-between mb-1">
                                <h2 className="text-3xl font-black text-gray-900 tracking-tight">Analytics</h2>
                                <div className="relative flex items-center justify-center w-8 h-8">
                                    <span className="absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-30 animate-ping"></span>
                                    <span className="relative inline-flex rounded-full h-3 w-3 bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.8)]"></span>
                                </div>
                            </div>
                            <p className="text-xs font-bold uppercase tracking-widest text-indigo-400">Multi-Camera Trajectory</p>
                        </div>
                        
                        {/* QUICK SEARCH */}
                        <div className="mb-8">
                            <div className="relative">
                                <input 
                                    type="text" 
                                    placeholder="Trace License Plate (Enter)..." 
                                    className="w-full bg-white border-2 border-transparent focus:border-indigo-500 rounded-2xl px-5 py-3.5 text-sm font-bold text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400"
                                    value={plateSearch} 
                                    onChange={e => setPlateSearch(e.target.value.toUpperCase())}
                                    onKeyDown={handleSearch}
                                />
                                <div className="absolute right-4 top-3.5 text-gray-400">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                </div>
                            </div>
                        </div>
                        
                        {/* TELEMETRY */}
                        <div className="mb-8 flex-shrink-0">
                            <h2 className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest">System Health</h2>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-gradient-to-br from-white to-gray-50 p-5 rounded-2xl border border-indigo-50 shadow-[0_10px_30px_rgba(99,102,241,0.08)] flex flex-col justify-center relative overflow-hidden group">
                                    <div className="absolute inset-0 radar-sweep pointer-events-none"></div>
                                    <div className="absolute -right-4 -bottom-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
                                    </div>
                                    <div className="text-gray-400 text-[10px] font-black uppercase tracking-widest mb-1 relative z-10">PaddleOCR Engine</div>
                                    <div className="text-3xl text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-400 font-black relative z-10">98.9%</div>
                                </div>
                                <div className="bg-gradient-to-br from-white to-gray-50 p-5 rounded-2xl border border-gray-100 shadow-[0_8px_20px_rgba(0,0,0,0.03)] flex flex-col justify-center">
                                    <div className="text-gray-400 text-[10px] font-black uppercase tracking-widest mb-3">Node Status</div>
                                    {(!telemetry || !telemetry.cameras || telemetry.cameras.length === 0) ? <span className="text-sm font-bold text-rose-500 bg-rose-50 px-2 py-1 rounded w-max">Offline</span> : telemetry.cameras.map(c => (
                                        <div key={c.camera_id} className="flex items-center mt-1.5 text-xs font-bold text-gray-700">
                                            <div className={`w-2.5 h-2.5 rounded-full mr-2 shadow-sm ${c.status === 'online' ? 'bg-emerald-500 shadow-emerald-500/50 animate-pulse' : 'bg-rose-500 shadow-rose-500/50'}`}></div>
                                            {c.camera_id}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* ACTIONS (Upload) */}
                        <div className="flex-shrink-0 mt-auto">
                            <h2 className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest">Ingest Video Feeds</h2>
                            <div className="space-y-3 mb-5">
                                {[1, 2, 3].map(num => (
                                    <div key={num} className="relative group">
                                        <input type="file" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" onChange={e => setFiles({...files, [`cam${num}`]: e.target.files[0]})} />
                                        <div className={`flex items-center justify-between p-3 rounded-2xl border-2 transition-all ${files[`cam${num}`] ? 'bg-indigo-50 border-indigo-200' : 'bg-white border-gray-100 group-hover:border-indigo-100 group-hover:bg-indigo-50/30'}`}>
                                            <div className="flex items-center">
                                                <div className={`p-2 rounded-xl mr-3 ${files[`cam${num}`] ? 'bg-indigo-500 text-white shadow-md shadow-indigo-500/30' : 'bg-gray-100 text-gray-400 group-hover:bg-indigo-100 group-hover:text-indigo-500'}`}>
                                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                </div>
                                                <div>
                                                    <div className="text-xs font-black text-gray-700">Camera {num}</div>
                                                    <div className="text-[10px] font-bold text-gray-400 truncate w-32">{files[`cam${num}`] ? files[`cam${num}`].name : 'Select video file...'}</div>
                                                </div>
                                            </div>
                                            {files[`cam${num}`] && (
                                                <div className="w-5 h-5 bg-emerald-500 rounded-full flex items-center justify-center text-white shadow-sm shadow-emerald-500/30">
                                                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <button onClick={handleUpload} className="w-full bg-gradient-to-r from-indigo-600 to-blue-500 hover:from-indigo-700 hover:to-blue-600 text-white py-4 rounded-2xl text-sm font-black uppercase tracking-wider shadow-xl shadow-indigo-500/30 transition-transform transform hover:-translate-y-1 flex justify-center items-center group">
                                <span className="group-hover:animate-pulse mr-2">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                                </span>
                                Start AI Pipeline
                            </button>
                            {status && <div className="text-[10px] text-center font-black uppercase tracking-widest text-indigo-600 mt-4 bg-indigo-50/50 p-2 rounded-xl">{status}</div>}
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

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ErrorBoundary><Dashboard /></ErrorBoundary>);

    