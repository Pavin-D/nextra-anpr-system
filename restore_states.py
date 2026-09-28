import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace everything from 'function Dashboard() {' down to the 'return (' statement.
start_idx = content.find("function Dashboard() {")
end_idx = content.find("            return (\n                <div className=")

if start_idx != -1 and end_idx != -1:
    correct_states = """function Dashboard() {
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

                    // Fix 3 predefined camera nodes on the map permanently
                    const camIcon = L.icon({
                        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
                    });
                    
                    L.marker([28.6315, 77.2167], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_01</b><br>Connaught Place North');
                    L.marker([28.6258, 77.2343], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_02</b><br>Mandi House Circle');
                    L.marker([28.6129, 77.2295], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_03</b><br>India Gate Roundabout');
                }

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

"""
    final_content = content[:start_idx] + correct_states + content[end_idx:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("Rewrote Dashboard states flawlessly.")
else:
    print("Could not find bounds.")
