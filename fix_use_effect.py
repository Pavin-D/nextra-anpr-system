import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the entire React.useEffect block for map and telemetry.
# First, let's find the bounds.
start_idx = content.find("            React.useEffect(() => {")
# Find the end of handleSearch to know where the next block starts, then back up.
end_idx = content.find("            const handleSearch = async (e) => {")

if start_idx != -1 and end_idx != -1:
    correct_use_effect = """            React.useEffect(() => {
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

"""
    final_content = content[:start_idx] + correct_use_effect + content[end_idx:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("Rewrote useEffect cleanly!")
else:
    print("Could not find bounds.")
