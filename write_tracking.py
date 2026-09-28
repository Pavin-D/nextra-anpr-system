import re

with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

# We will extract VoiceNav and the CSS style block from index.html to reuse it.
voice_nav_match = re.search(r'(const VoiceNav = \(\) => \{.*?\n        \};)', index_content, re.DOTALL)
voice_nav_code = voice_nav_match.group(1) if voice_nav_match else ""

style_match = re.search(r'(<style>.*?</style>)', index_content, re.DOTALL)
style_code = style_match.group(1) if style_match else ""

tracking_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXTRA - Vehicle Tracking</title>
    <!-- React & Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Leaflet JS & CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    {style_code}
</head>
<body class="bg-gray-100 text-gray-900 font-sans min-h-screen">
    <div id="root"></div>
    
    <script type="text/babel">
{voice_nav_code}

function TrackingApp() {{
    const [plateSearch, setPlateSearch] = React.useState('');
    const [status, setStatus] = React.useState('');
    const [knownPlates, setKnownPlates] = React.useState([]);
    const [isSearching, setIsSearching] = React.useState(false);
    const [showSidebar, setShowSidebar] = React.useState(true);
    
    const mapRef = React.useRef(null);
    const mapInstance = React.useRef(null);
    const trajectoryLayer = React.useRef(null);

    React.useEffect(() => {{
        if (!mapInstance.current && mapRef.current) {{
            mapInstance.current = L.map(mapRef.current, {{ zoomControl: false }}).setView([28.6200, 77.2260], 14);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; OpenStreetMap contributors'
            }}).addTo(mapInstance.current);
            
            L.control.zoom({{ position: 'bottomright' }}).addTo(mapInstance.current);
            trajectoryLayer.current = L.layerGroup().addTo(mapInstance.current);
            setTimeout(() => {{ if (mapInstance.current) mapInstance.current.invalidateSize(); }}, 500);
            
            const camIcon = L.icon({{
                iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
            }});
            
            L.marker([28.6315, 77.2167], {{icon: camIcon}}).addTo(mapInstance.current).bindPopup('<b>CAM_01</b><br>Connaught Place North');
            L.marker([28.6258, 77.2343], {{icon: camIcon}}).addTo(mapInstance.current).bindPopup('<b>CAM_02</b><br>Mandi House Circle');
            L.marker([28.6129, 77.2295], {{icon: camIcon}}).addTo(mapInstance.current).bindPopup('<b>CAM_03</b><br>India Gate Roundabout');
        }}
        
        fetch('/api/v1/plates')
            .then(r => r.json())
            .then(data => setKnownPlates(data.plates || []))
            .catch(e => console.error("Error fetching plates", e));
    }}, []);

    const searchTrajectory = async (plateOverride) => {{
        const plate = typeof plateOverride === 'string' ? plateOverride : plateSearch;
        if (!plate) return;
        setPlateSearch(plate.toUpperCase());
        trajectoryLayer.current.clearLayers();
        setStatus("Tracing optimal path...");
        setIsSearching(true);
        try {{
            const res = await fetch(`/api/v1/trajectory/${{plate.toUpperCase()}}`);
            const data = await res.json();
            if (!data.trajectory || data.trajectory.length === 0) {{
                setStatus(`No detections found for ${{plate}}`);
                setIsSearching(false);
                return;
            }}
            const latlngs = data.trajectory.map(p => [p.lat, p.long]);
            
            if (latlngs.length > 1) {{
                try {{
                    const coords = data.trajectory.map(p => `${{p.long}},${{p.lat}}`).join(';');
                    const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${{coords}}?overview=full&geometries=geojson&alternatives=true`;
                    const osrmRes = await fetch(osrmUrl);
                    const osrmData = await osrmRes.json();
                    
                    if (osrmData.routes && osrmData.routes.length > 0) {{
                        for (let i = osrmData.routes.length - 1; i >= 0; i--) {{
                            const isOptimal = (i === 0);
                            L.geoJSON(osrmData.routes[i].geometry, {{
                                style: {{ 
                                    color: isOptimal ? '#4f46e5' : '#94a3b8', 
                                    weight: isOptimal ? 6 : 4, 
                                    opacity: isOptimal ? 0.9 : 0.6,
                                    dashArray: isOptimal ? '' : '8, 8'
                                }}
                            }}).addTo(trajectoryLayer.current);
                        }}
                    }} else {{
                        L.polyline(latlngs, {{color: '#4f46e5', weight: 6, dashArray: '10, 15'}}).addTo(trajectoryLayer.current);
                    }}
                }} catch (err) {{
                    L.polyline(latlngs, {{color: '#4f46e5', weight: 6, dashArray: '10, 15'}}).addTo(trajectoryLayer.current);
                }}
            }}

            data.trajectory.forEach((p, index) => {{
                L.circleMarker([p.lat, p.long], {{color: '#ec4899', fillColor: '#ec4899', radius: 8, fillOpacity: 1}})
                 .bindPopup(`<b>${{p.location_name || 'Node'}}</b><br/>Time: ${{new Date(p.timestamp).toLocaleTimeString()}}`)
                 .addTo(trajectoryLayer.current).openPopup();
            }});
            mapInstance.current.fitBounds(trajectoryLayer.current.getBounds(), {{padding: [100, 100]}});
            setStatus(`Successfully mapped ${{latlngs.length}} nodes.`);
        }} catch (e) {{ 
            setStatus("Error loading trajectory network."); 
        }}
        setIsSearching(false);
        if(window.innerWidth < 768) setShowSidebar(false);
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
                        <a href="/tracking" className="px-5 py-2 text-xs font-black uppercase tracking-wider rounded-xl bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-lg shadow-indigo-500/30 transition-transform transform hover:-translate-y-0.5">Tracking</a>
                        <a href="/blacklist" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Blacklist</a>
                        <a href="/geofence" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">Geofence</a>
                        <a href="/chat" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-gray-500 hover:text-indigo-600 hover:bg-indigo-50/50 transition-colors">AI Chat</a>
                        <a href="/alerts" className="px-5 py-2 text-xs font-bold uppercase tracking-wider rounded-xl text-rose-500 hover:bg-rose-50 transition-colors">Alerts</a>
                    </div>
                </div>
            </div>
            
            {{/* FLOATING SIDEBAR */}}
            <div className={{`absolute top-28 left-6 bottom-6 w-[400px] max-w-[90vw] z-[900] rounded-3xl bg-gradient-to-br from-fuchsia-500 via-cyan-400 to-indigo-500 p-[2px] shadow-[0_0_30px_rgba(34,211,238,0.4)] transform transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${{showSidebar ? 'translate-x-0' : '-translate-x-[120%]'}}`}}>
                <div className="w-full h-full bg-white/90 backdrop-blur-3xl p-8 flex flex-col rounded-[22px] overflow-y-auto relative">
                    <div className="mb-8">
                        <div className="flex items-center justify-between mb-1">
                            <h2 className="text-3xl font-black text-gray-900 tracking-tight">Tracking</h2>
                            <div className="relative flex items-center justify-center w-8 h-8">
                                <span className="absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-30 animate-ping"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500 shadow-[0_0_10px_rgba(34,211,238,0.8)]"></span>
                            </div>
                        </div>
                        <p className="text-xs font-bold uppercase tracking-widest text-indigo-400">Advanced Trajectory Map</p>
                    </div>
                    
                    {{/* QUICK SEARCH */}}
                    <div className="mb-8">
                        <div className="relative">
                            <input 
                                type="text" 
                                placeholder="Enter Target Plate (e.g. DL2CQ3150)" 
                                className="w-full bg-white border-2 border-transparent focus:border-indigo-500 rounded-2xl px-5 py-4 text-sm font-bold text-gray-800 shadow-sm outline-none transition-all placeholder-gray-400 uppercase"
                                value={{plateSearch}} 
                                onChange={{e => setPlateSearch(e.target.value)}}
                                onKeyDown={{e => e.key === 'Enter' && searchTrajectory()}}
                            />
                            <button onClick={{() => searchTrajectory()}} className="absolute right-3 top-3 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 p-2 rounded-xl transition-colors">
                                <svg className={{`w-5 h-5 ${{isSearching ? 'animate-spin' : ''}}`}} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                            </button>
                        </div>
                        {{status && <p className="text-[10px] font-black uppercase tracking-widest text-indigo-600 mt-4 bg-indigo-50/50 p-2 rounded-xl text-center">{{status}}</p>}}
                    </div>
                    
                    {{/* DATABASE RECORDS */}}
                    <div className="mb-8 flex-shrink-0">
                        <h2 className="text-[10px] font-black text-gray-400 mb-4 uppercase tracking-widest border-b border-gray-100 pb-2">Active Network Entities</h2>
                        <div className="flex flex-wrap gap-2">
                            {{knownPlates.length === 0 ? (
                                <span className="text-xs text-gray-400 italic font-bold">Awaiting telemetry...</span>
                            ) : (
                                knownPlates.map((p, i) => (
                                    <button 
                                        key={{i}} 
                                        onClick={{() => searchTrajectory(p)}}
                                        className="px-3 py-1.5 bg-gray-50 border border-gray-100 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 text-xs text-gray-600 rounded-lg font-mono font-black shadow-sm transition-all transform hover:-translate-y-0.5">
                                        {{p}}
                                    </button>
                                ))
                            )}}
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
root.render(<ErrorBoundary><TrackingApp /></ErrorBoundary>);
</script>
</body>
</html>"""

with open("tracking.html", "w", encoding="utf-8") as f:
    f.write(tracking_html)

print("Rewrote tracking.html completely with the perfect advanced white UI.")
