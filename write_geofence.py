import re

with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

# Extract VoiceNav
voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', index_content, re.DOTALL)
voice_nav_code = voice_nav_match.group(1) if voice_nav_match else ""

# The basic HTML shell
geofence_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - Geofence Analytics</title>
    <!-- React & Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Leaflet & Draw -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
    <script src="https://unpkg.com/@turf/turf@6/turf.min.js"></script>

    <style>
        .custom-scrollbar::-webkit-scrollbar {{ width: 6px; }}
        .custom-scrollbar::-webkit-scrollbar-track {{ background: transparent; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background-color: #cbd5e1; border-radius: 10px; }}
        @keyframes fade-in {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        /* Restyle Leaflet Draw Controls for modern look */
        .leaflet-draw-toolbar a {{ background-color: #fff !important; color: #4f46e5 !important; border: 1px solid #e2e8f0 !important; }}
        .leaflet-draw-toolbar a:hover {{ background-color: #eef2ff !important; }}
    </style>
</head>
<body class="bg-gray-100 text-gray-900 font-sans min-h-screen">
    <div id="root"></div>
    
    <script type="text/babel">
{voice_nav_code}

const CAMERAS = [
    {{id: 'CAM_01', lat: 28.6304, lng: 77.2177}},
    {{id: 'CAM_02', lat: 28.6129, lng: 77.2295}},
    {{id: 'CAM_03', lat: 28.6145, lng: 77.2021}},
    {{id: 'CAM_04', lat: 28.6250, lng: 77.2000}},
    {{id: 'CAM_05', lat: 28.6350, lng: 77.2300}}
];

function GeofenceApp() {{
    const [detections, setDetections] = React.useState([]);
    const [status, setStatus] = React.useState('Draw a geofence on the map to scan area.');
    const [activeCameras, setActiveCameras] = React.useState([]);
    const [showSidebar, setShowSidebar] = React.useState(true);
    const [isScanning, setIsScanning] = React.useState(false);

    const mapRef = React.useRef(null);
    const mapInstance = React.useRef(null);
    const drawnItems = React.useRef(null);

    React.useEffect(() => {{
        if (!mapInstance.current && mapRef.current) {{
            mapInstance.current = L.map(mapRef.current, {{ zoomControl: false }}).setView([28.6200, 77.2260], 14);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; OpenStreetMap'
            }}).addTo(mapInstance.current);
            
            L.control.zoom({{ position: 'bottomright' }}).addTo(mapInstance.current);
            setTimeout(() => {{ if (mapInstance.current) mapInstance.current.invalidateSize(); }}, 500);

            // Add fixed cameras
            const camIcon = L.icon({{
                iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                iconSize: [25, 41], iconAnchor: [12, 41]
            }});
            
            CAMERAS.forEach(cam => {{
                L.marker([cam.lat, cam.lng], {{icon: camIcon}})
                 .addTo(mapInstance.current)
                 .bindTooltip(`<b>${{cam.id}}</b>`, {{permanent: true, direction: 'top', offset: [0,-40], className: 'font-mono text-[10px] font-black tracking-widest bg-indigo-600 text-white border-0 shadow-lg px-2 py-1 rounded'}});
            }});

            // Initialize Draw Feature
            drawnItems.current = new L.FeatureGroup();
            mapInstance.current.addLayer(drawnItems.current);
            
            const drawControl = new L.Control.Draw({{
                position: 'topright',
                edit: {{ featureGroup: drawnItems.current, remove: true }},
                draw: {{
                    polygon: {{ shapeOptions: {{ color: '#f43f5e', weight: 4, fillOpacity: 0.2, dashArray: '10, 10' }} }},
                    rectangle: {{ shapeOptions: {{ color: '#f43f5e', weight: 4, fillOpacity: 0.2, dashArray: '10, 10' }} }},
                    circle: {{ shapeOptions: {{ color: '#f43f5e', weight: 4, fillOpacity: 0.2, dashArray: '10, 10' }} }},
                    polyline: false, marker: false, circlemarker: false
                }}
            }});
            mapInstance.current.addControl(drawControl);

            mapInstance.current.on(L.Draw.Event.CREATED, function (e) {{
                const layer = e.layer;
                drawnItems.current.addLayer(layer);
                analyzeAllGeofences();
            }});
            
            mapInstance.current.on(L.Draw.Event.DELETED, function (e) {{
                analyzeAllGeofences();
            }});
            
            mapInstance.current.on(L.Draw.Event.EDITED, function (e) {{
                analyzeAllGeofences();
            }});
        }}
    }}, []);

    const analyzeAllGeofences = async () => {{
        setIsScanning(true);
        setStatus('Analyzing restricted areas...');
        
        const insideCameras = new Set();
        
        drawnItems.current.eachLayer(layer => {{
            let polyGeoJson;
            if (layer instanceof L.Circle) {{
                const center = [layer.getLatLng().lng, layer.getLatLng().lat];
                const radius = layer.getRadius() / 1000;
                polyGeoJson = turf.circle(center, radius, {{steps: 64, units: 'kilometers'}});
            }} else {{
                polyGeoJson = layer.toGeoJSON();
            }}

            CAMERAS.forEach(cam => {{
                const pt = turf.point([cam.lng, cam.lat]);
                if (turf.booleanPointInPolygon(pt, polyGeoJson)) {{
                    insideCameras.add(cam.id);
                }}
            }});
        }});

        const cameraArray = Array.from(insideCameras);
        setActiveCameras(cameraArray);

        if (cameraArray.length === 0) {{
            setStatus('No cameras detected in marked zones.');
            setDetections([]);
            setIsScanning(false);
            return;
        }}

        setStatus(`Querying nodes: ${{cameraArray.join(', ')}}`);
        
        try {{
            const res = await fetch('/api/v1/geofence-search', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{cameras: cameraArray}})
            }});
            const data = await res.json();
            setDetections(data.detections || []);
            setStatus(`Identified ${{data.detections.length}} vehicles.`);
        }} catch (e) {{
            setStatus('Error establishing node uplink.');
            setDetections([]);
        }}
        setIsScanning(false);
    }};

    return (
        <div className="relative w-full h-screen overflow-hidden bg-gray-100 font-sans text-gray-900">
            
            {{/* MAP BACKGROUND */}}
            <div ref={{mapRef}} id="main-map" style={{{{position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, width: '100vw', height: '100vh', zIndex: 10}}}}></div>

            {{/* FLOATING TOP NAVIGATION BAR */}}
            <div className="absolute top-6 left-6 right-6 z-[1000] rounded-2xl bg-gradient-to-r from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_25px_rgba(34,211,238,0.4)] transition-all">
                <div className="h-16 w-full bg-white/90 backdrop-blur-3xl rounded-[14px] flex items-center px-6 justify-between">
                    <div className="flex items-center space-x-4">
                        <button onClick={{() => setShowSidebar(!showSidebar)}} className="text-gray-500 hover:text-indigo-600 transition-colors p-2 rounded-full hover:bg-indigo-50/50">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                        </button>
                        <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500 tracking-tight">NEXTRA</h1>
                        <VoiceNav />
                    </div>
                    <div className="hidden md:flex space-x-2">
                        <a href="/" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Dashboard</a>
                        <a href="/tracking" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Tracking</a>
                        <a href="/blacklist" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                        <a href="/geofence" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Geofence</a>
                        <a href="/chat" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                        <a href="/alerts" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    </div>
                </div>
            </div>
            
            {{/* FLOATING SIDEBAR */}}
            <div className={{`absolute top-28 left-6 bottom-6 w-[450px] max-w-[90vw] z-[900] rounded-3xl bg-gradient-to-br from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_30px_rgba(34,211,238,0.4)] transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${{showSidebar ? 'translate-x-0' : '-translate-x-[120%]'}}`}}>
                <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-[22px] overflow-hidden relative">
                    <div className="flex-shrink-0 mb-6">
                        <div className="flex items-center justify-between mb-1">
                            <h2 className="text-3xl font-black text-gray-900 tracking-tight">Geofence</h2>
                            <div className="relative flex items-center justify-center w-8 h-8">
                                <span className={{`absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-30 ${{isScanning ? 'animate-ping' : ''}}`}}></span>
                                <span className={{`relative inline-flex rounded-full h-3 w-3 ${{isScanning ? 'bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.8)]' : 'bg-gray-400'}}`}}></span>
                            </div>
                        </div>
                        <p className="text-xs font-bold uppercase tracking-widest text-rose-400">Spatial Analytics Engine</p>
                    </div>
                    
                    {{/* STATUS INDICATOR */}}
                    <div className="flex-shrink-0 mb-6">
                        <div className="bg-gray-50 rounded-2xl p-4 border border-gray-100 flex items-center justify-between">
                            <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Scanner Status</span>
                            <span className={{`text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-md border ${{isScanning ? 'bg-indigo-50 text-indigo-600 border-indigo-200' : 'bg-white text-gray-400 border-gray-200'}}`}}>
                                {{status}}
                            </span>
                        </div>
                    </div>

                    {{/* ACTIVE NODES */}}
                    <div className="flex-shrink-0 mb-6">
                        <h2 className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest border-b border-gray-100 pb-2">Engaged Nodes</h2>
                        <div className="flex flex-wrap gap-2">
                            {{activeCameras.length === 0 ? (
                                <span className="text-xs text-gray-400 italic font-bold">Draw zone to engage nodes.</span>
                            ) : (
                                activeCameras.map((cam, i) => (
                                    <div key={{i}} className="px-3 py-1.5 bg-indigo-50 border border-indigo-100 text-indigo-700 text-[10px] rounded-lg font-mono font-black shadow-sm flex items-center" style={{{{animation: `fade-in 0.3s ease-out ${{i * 0.05}}s both`}}}}>
                                        <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 mr-2 animate-pulse shadow-[0_0_8px_rgba(99,102,241,0.8)]"></div>
                                        {{cam}}
                                    </div>
                                ))
                            )}}
                        </div>
                    </div>
                    
                    {{/* DETECTIONS TABLE */}}
                    <div className="flex-1 flex flex-col min-h-0">
                        <h2 className="text-[10px] font-black text-gray-400 mb-3 uppercase tracking-widest border-b border-gray-100 pb-2 flex-shrink-0">Zone Detections ({{detections.length}})</h2>
                        <div className="overflow-y-auto custom-scrollbar flex-1 pr-2 relative">
                            <div className="space-y-3">
                                {{detections.length === 0 ? (
                                    <div className="px-4 py-8 text-center text-gray-400 font-bold italic bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center">
                                        <svg className="w-8 h-8 mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                        No telemetry captured
                                    </div>
                                ) : (
                                    detections.map((d, i) => (
                                        <div key={{i}} className="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md hover:border-indigo-100 transition-all duration-300 group flex items-center justify-between" style={{{{animation: `fade-in 0.4s ease-out ${{i * 0.05}}s both`}}}}>
                                            <div>
                                                <div className="font-mono font-black text-cyan-500 tracking-wider text-sm mb-1 flex items-center">
                                                    {{d.plate_number}}
                                                </div>
                                                <div className="text-[10px] font-bold text-gray-400 flex items-center bg-gray-50 px-2 py-0.5 rounded border border-gray-100 w-max">
                                                    <svg className="w-3 h-3 mr-1 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                                    {{d.camera_id}}
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-xs font-black text-gray-700 group-hover:text-indigo-900 transition-colors">
                                                    {{new Date(d.timestamp).toLocaleTimeString(undefined, {{timeStyle: 'short'}})}}
                                                </div>
                                                <div className="text-[9px] font-bold text-gray-400 uppercase tracking-widest">
                                                    {{new Date(d.timestamp).toLocaleDateString(undefined, {{dateStyle: 'medium'}})}}
                                                </div>
                                            </div>
                                        </div>
                                    ))
                                )}}
                            </div>
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
root.render(<ErrorBoundary><GeofenceApp /></ErrorBoundary>);
</script>
</body>
</html>"""

with open("geofence.html", "w", encoding="utf-8") as f:
    f.write(geofence_html)

print("Rewrote geofence.html completely!")
