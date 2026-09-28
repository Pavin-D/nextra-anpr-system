import re

with open('geofence.html', 'r', encoding='utf-8') as f:
    content = f.read()

camera_data = """
        const CAMERAS = [
            {id: 'CAM_01', lat: 28.6304, lng: 77.2177},
            {id: 'CAM_02', lat: 28.6129, lng: 77.2295},
            {id: 'CAM_03', lat: 28.6145, lng: 77.2021},
            {id: 'CAM_04', lat: 28.6250, lng: 77.2000},
            {id: 'CAM_05', lat: 28.6350, lng: 77.2300}
        ];
"""

if "const CAMERAS =" not in content:
    content = content.replace('function GeofenceApp() {', camera_data + '\n        function GeofenceApp() {')

    with open('geofence.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
print("CAMERAS array injected successfully.")
