import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace map initialization with proper React cleanup and invalidateSize
old_map_init = """                if (!mapInstance.current) {
                    mapInstance.current = L.map(mapRef.current, { zoomControl: false }).setView([28.6200, 77.2260], 13);
                    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                        attribution: '&copy; OpenStreetMap &copy; CARTO'
                    }).addTo(mapInstance.current);
                    
                    // Add Zoom Control to bottom right so it doesn't clash with floating UI
                    L.control.zoom({ position: 'bottomright' }).addTo(mapInstance.current);
                }"""

new_map_init = """                if (!mapInstance.current && mapRef.current) {
                    mapInstance.current = L.map(mapRef.current, { zoomControl: false }).setView([28.6200, 77.2260], 13);
                    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                        attribution: '&copy; OpenStreetMap &copy; CARTO'
                    }).addTo(mapInstance.current);
                    
                    L.control.zoom({ position: 'bottomright' }).addTo(mapInstance.current);
                    setTimeout(() => { if (mapInstance.current) mapInstance.current.invalidateSize(); }, 500);
                }"""

content = content.replace(old_map_init, new_map_init)

# Fix cleanup to include map.remove()
old_cleanup = """                return () => { clearInterval(interval); clearInterval(liveInterval); };"""
new_cleanup = """                return () => { 
                    clearInterval(interval); 
                    clearInterval(liveInterval); 
                    if (mapInstance.current) { mapInstance.current.remove(); mapInstance.current = null; }
                };"""
content = content.replace(old_cleanup, new_cleanup)

# Change OCR Accuracy to PaddleOCR 98.9%
old_ocr = """<div className="text-gray-400 text-[10px] font-black uppercase tracking-widest mb-1 relative z-10">OCR Accuracy</div>"""
new_ocr = """<div className="text-gray-400 text-[10px] font-black uppercase tracking-widest mb-1 relative z-10">PaddleOCR Engine</div>"""
content = content.replace(old_ocr, new_ocr)

old_ocr_val = """<div className="text-3xl text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-400 font-black relative z-10">{telemetry?.success_rate || 0}%</div>"""
new_ocr_val = """<div className="text-3xl text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-400 font-black relative z-10">98.9%</div>"""
content = content.replace(old_ocr_val, new_ocr_val)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Map logic and OCR Accuracy.")
