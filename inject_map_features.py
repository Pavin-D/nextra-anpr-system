import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject the markers inside map initialization
map_init_pattern = r"(mapInstance\.current = L\.map\(mapRef\.current.*?\n.*?invalidateSize\(\);\s*\}\s*,\s*500\);\s*\})"

markers_injection = """
                    // Fix 3 predefined camera nodes on the map permanently
                    const camIcon = L.icon({
                        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
                        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
                        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34]
                    });
                    
                    L.marker([28.6315, 77.2167], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_01</b><br>Connaught Place North');
                    L.marker([28.6258, 77.2343], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_02</b><br>Mandi House Circle');
                    L.marker([28.6129, 77.2295], {icon: camIcon}).addTo(mapInstance.current).bindPopup('<b>CAM_03</b><br>India Gate Roundabout');
"""

def repl_map(m):
    return m.group(1) + markers_injection

content = re.sub(map_init_pattern, repl_map, content, flags=re.DOTALL)


# 2. Inject the heatmap into fetchTelemetry
fetch_telemetry_pattern = r"(const fetchTelemetry = async \(\) => \{\s*try \{)(.*?)(if \(data\.alerts\) setAlerts\(data\.alerts\);\s*\}(.*?)catch \(e\) \{ console\.error\(e\); \}\s*\};)"

heatmap_injection = """
                        // Heatmap logic
                        const heatRes = await fetch('/api/v1/analytics/heatmap');
                        const heatData = await heatRes.json();
                        if (heatLayer.current) mapInstance.current.removeLayer(heatLayer.current);
                        if (heatData.heatmap) {
                            const heatPoints = heatData.heatmap.map(c => [c.lat, c.long, c.detection_count * 10]);
                            heatLayer.current = L.heatLayer(heatPoints, {radius: 40, blur: 20}).addTo(mapInstance.current);
                        }
"""

def repl_telemetry(m):
    return m.group(1) + m.group(2) + "if (data.alerts) setAlerts(data.alerts);\n" + heatmap_injection + "\n} catch(e) { console.error(e); };"

content = re.sub(fetch_telemetry_pattern, repl_telemetry, content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Injected map markers and heatmap logic")
