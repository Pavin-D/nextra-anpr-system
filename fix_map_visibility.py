import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Make the map div absolutely foolproof
old_map_div = """                    {/* MAP BACKGROUND */}
                    <div className="absolute inset-0 z-0">
                        <div ref={mapRef} style={{height: '100%', width: '100%'}}></div>
                    </div>"""

new_map_div = """                    {/* MAP BACKGROUND */}
                    <div ref={mapRef} id="main-map" style={{position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, width: '100vw', height: '100vh', zIndex: 10}}></div>"""

content = content.replace(old_map_div, new_map_div)

# Change tile layer to standard OSM in case Carto is blocked
old_tile = "'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'"
new_tile = "'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'"
content = content.replace(old_tile, new_tile)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Map div and tiles")
