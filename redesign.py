import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

new_content = """            const handleUpload = async () => {
                setStatus("Uploading feeds to multi-pipeline...");
                setShowLivePreview(true);
                setShowSidebar(false); // Auto-hide sidebar to view processing
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
                <div className="flex flex-col h-screen overflow-hidden bg-gray-50 text-gray-900 font-sans">
                    
                    {/* TOP NAVIGATION BAR */}
                    <div className="h-16 bg-white border-b border-gray-200 flex items-center px-6 justify-between z-[1000] shadow-sm flex-shrink-0">
                        <div className="flex items-center space-x-4">
                            <button onClick={() => setShowSidebar(!showSidebar)} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                            </button>
                            <h1 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                            <VoiceNav />
                        </div>
                        <div className="hidden md:flex space-x-1 border border-gray-200 rounded-lg p-1 bg-gray-50">
                            <a href="/" className="px-4 py-1.5 text-sm font-bold rounded-md bg-white text-indigo-700 shadow-sm border border-gray-200">Dashboard Overview</a>
                            <a href="/tracking" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Vehicle Tracking</a>
                            <a href="/blacklist" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Blacklist Manager</a>
                            <a href="/geofence" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">Geofence Analytics</a>
                            <a href="/chat" className="px-4 py-1.5 text-sm font-semibold rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-200 transition-colors">AI Chat Search</a>
                        </div>
                    </div>

                    <div className="flex flex-1 overflow-hidden relative">
                    
                    {/* LIVE AI PREVIEW MODAL */}
                    {showLivePreview && (
                        <div className="absolute top-6 right-6 w-96 bg-white border border-gray-200 rounded-2xl shadow-2xl overflow-hidden z-[999] ring-1 ring-black ring-opacity-5">
                            <div className="bg-gradient-to-r from-indigo-600 to-blue-500 px-5 py-3 flex justify-between items-center">
                                <h3 className="font-bold text-sm text-white tracking-wide">LIVE AI ENGINE</h3>
                                <button onClick={() => setShowLivePreview(false)} className="text-white/80 hover:text-white font-bold text-lg leading-none">&times;</button>
                            </div>
                            <div className="p-3 relative bg-gray-50">
                                <img src={liveImgUrl} alt="AI Stream" className="w-full h-auto rounded-lg shadow-inner min-h-[200px] object-cover bg-gray-200" onError={(e) => e.target.src=''} />
                                <div className="absolute top-5 left-5 bg-black/60 backdrop-blur-sm px-2 py-1 rounded shadow text-xs text-emerald-400 font-mono flex items-center">
                                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse mr-2"></span>[YOLOv11] Tracking...
                                </div>
                            </div>
                            <div className="p-5 bg-white border-t border-gray-100">
                                <div className="flex justify-between text-xs font-semibold text-gray-600 mb-2">
                                    <span>Processing Video Feeds...</span>
                                    <span className="text-indigo-600">{aiProgress}%</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                                    <div className="bg-gradient-to-r from-indigo-500 to-blue-500 h-2.5 rounded-full transition-all duration-300 ease-out" style={{width: `${aiProgress}%`}}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    {/* Sidebar / Controls */}
                    <div className={`absolute top-0 left-0 h-full w-[400px] max-w-[90vw] bg-white/95 backdrop-blur-xl p-6 pt-8 flex flex-col shadow-[10px_0_30px_rgba(0,0,0,0.05)] z-[900] overflow-y-auto transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] border-r border-gray-100 ${showSidebar ? 'translate-x-0' : '-translate-x-full'}`}>
                        <div className="mb-8">
                            <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight mb-1">Analytics</h2>
                            <p className="text-sm text-gray-500 font-medium">Multi-Camera Trajectory & Vision</p>
                        </div>
                        
                        {/* LIVE ALERTS */}
                        <div className="mb-8 bg-rose-50 rounded-2xl border border-rose-100 p-5 shadow-sm">
                            <h2 className="text-sm font-bold text-rose-600 mb-3 flex items-center uppercase tracking-wider">
                                <span className="relative flex h-3 w-3 mr-2">
                                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                                  <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
                                </span>
                                Live Threat Alerts
                            </h2>
                            {(!alerts || alerts.length === 0) ? <p className="text-sm text-gray-500 font-medium">No active alerts detected.</p> : 
                                alerts.map(a => (
                                    <div key={a.id} className="text-sm mb-3 bg-white p-3 rounded-xl border border-rose-100 shadow-sm">
                                        <div className="font-bold text-gray-900 font-mono text-base">{a.plate_number}</div>
                                        <div className="text-gray-700 mt-1">{a.description}</div>
                                        <div className="text-rose-500 text-xs font-semibold mt-2 flex items-center">
                                            <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                                            {a.camera_id} @ {new Date(a.timestamp).toLocaleTimeString()}
                                        </div>
                                    </div>
                                ))
                            }
                        </div>
                        
                        {/* TELEMETRY */}
                        <div className="mb-8 flex-shrink-0">
                            <h2 className="text-xs font-bold text-gray-400 mb-3 uppercase tracking-wider">System Telemetry</h2>
                            <div className="grid grid-cols-2 gap-3">
                                <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 shadow-sm flex flex-col justify-center">
                                    <div className="text-gray-500 text-xs font-semibold mb-1">OCR Success</div>
                                    <div className="text-2xl text-indigo-600 font-black">{telemetry?.success_rate || 0}%</div>
                                </div>
                                <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 shadow-sm">
                                    <div className="text-gray-500 text-xs font-semibold mb-2">Node Status</div>
                                    {(!telemetry || !telemetry.cameras || telemetry.cameras.length === 0) ? <span className="text-sm text-gray-400">Offline</span> : telemetry.cameras.map(c => (
                                        <div key={c.camera_id} className="flex items-center mt-1 text-sm font-medium text-gray-700">
                                            <div className={`w-2.5 h-2.5 rounded-full mr-2 shadow-sm ${c.status === 'online' ? 'bg-emerald-500' : 'bg-rose-500'}`}></div>
                                            {c.camera_id}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* VEHICLE TRACKING (MOVED) */}
                        <div className="mb-8 flex-shrink-0">
                            <a href="/tracking" className="flex items-center justify-center w-full bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 text-indigo-700 border border-indigo-200 py-3.5 rounded-xl text-sm font-bold shadow-sm transition-all">
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724a1 1 0 01-.553-.894V4.152a1 1 0 011.447-.894L9 5.5l5.447-2.724a1 1 0 01.553.894v12.227a1 1 0 01-.447.894L15 20m0 0l-5.447-2.724a1 1 0 00-.894 0L3.5 20"></path></svg>
                                Open Detailed Tracking Map
                            </a>
                        </div>

                        {/* ACTIONS (Upload) */}
                        <div className="flex-shrink-0 pb-10">
                            <h2 className="text-xs font-bold text-gray-400 mb-3 uppercase tracking-wider">Video Ingestion</h2>
                            <div className="space-y-3 mb-5">
                                <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                    <label className="block text-xs font-bold text-gray-600 mb-1.5">CAM_01 Source</label>
                                    <input type="file" className="text-sm text-gray-600 w-full file:mr-3 file:py-1.5 file:px-3 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer" onChange={e => setFiles({...files, cam1: e.target.files[0]})} />
                                </div>
                                <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                    <label className="block text-xs font-bold text-gray-600 mb-1.5">CAM_02 Source</label>
                                    <input type="file" className="text-sm text-gray-600 w-full file:mr-3 file:py-1.5 file:px-3 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer" onChange={e => setFiles({...files, cam2: e.target.files[0]})} />
                                </div>
                                <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                    <label className="block text-xs font-bold text-gray-600 mb-1.5">CAM_03 Source</label>
                                    <input type="file" className="text-sm text-gray-600 w-full file:mr-3 file:py-1.5 file:px-3 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer" onChange={e => setFiles({...files, cam3: e.target.files[0]})} />
                                </div>
                            </div>
                            <button onClick={handleUpload} className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white py-3.5 rounded-xl text-sm font-bold shadow-md shadow-indigo-500/30 transition-all transform hover:-translate-y-0.5 flex justify-center items-center">
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                                Ingest Video Feeds
                            </button>
                            {status && <p className="text-sm text-center font-medium text-indigo-600 mt-4 bg-indigo-50 py-2 rounded-lg">{status}</p>}
                        </div>
                    </div>
                    
                    {/* Map Display */}
                    <div className="flex-1 bg-gray-100 relative h-full w-full" id="map-container">
                        <div ref={mapRef} style={{height: '100%', width: '100%', position: 'absolute', top: 0, left: 0, zIndex: 0}}></div>
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
"""

# Extract the old block to replace
start_idx = content.find("            const handleUpload = async () => {")
end_idx = content.find("        root.render(<ErrorBoundary><Dashboard /></ErrorBoundary>);") + len("        root.render(<ErrorBoundary><Dashboard /></ErrorBoundary>);")

if start_idx != -1 and end_idx != -1:
    final_content = content[:start_idx] + new_content + content[end_idx:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("UI completely redesigned to beautiful white theme.")
else:
    print("Could not find replacement bounds!")

