import re

with open("geofence.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the shapeOptions color to '#b91c1c' (darker red)
content = content.replace("color: '#f43f5e'", "color: '#b91c1c'")

# 2. Add trajectoryLayer to states
state_old = "    const drawnItems = React.useRef(null);"
state_new = "    const drawnItems = React.useRef(null);\n    const trajectoryLayer = React.useRef(null);"
content = content.replace(state_old, state_new)

# 3. Add to mapInstance initialization
init_old = "            drawnItems.current = new L.FeatureGroup();"
init_new = "            trajectoryLayer.current = L.layerGroup().addTo(mapInstance.current);\n            drawnItems.current = new L.FeatureGroup();"
content = content.replace(init_old, init_new)

# 4. Insert the viewVehicle function right before return
view_vehicle_code = """
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
"""
content = content.replace("    return (\n        <div className=\"relative", view_vehicle_code + "\n    return (\n        <div className=\"relative")

# 5. Add "View" button to the card
card_old = """                                            <div className="flex justify-between items-end border-t border-gray-50 pt-2 mt-auto">
                                                <div className="text-[9px] font-bold text-gray-400 uppercase tracking-widest">
                                                    {new Date(d.timestamp).toLocaleDateString(undefined, {dateStyle: 'short'})}
                                                </div>
                                                <div className="text-[10px] font-black text-gray-700 group-hover:text-indigo-900 transition-colors">
                                                    {new Date(d.timestamp).toLocaleTimeString(undefined, {timeStyle: 'short'})}
                                                </div>
                                            </div>
                                        </div>"""

card_new = """                                            <div className="flex justify-between items-end border-t border-gray-50 pt-2 mt-auto mb-2">
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
                                        </div>"""

content = content.replace(card_old, card_new)

with open("geofence.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Added View button and Map Trajectory support, changed geofence color!")
