import re

with open("geofence.html", "r", encoding="utf-8") as f:
    content = f.read()

old_cameras = """const CAMERAS = [
    {id: 'CAM_01', lat: 28.6304, lng: 77.2177},
    {id: 'CAM_02', lat: 28.6129, lng: 77.2295},
    {id: 'CAM_03', lat: 28.6145, lng: 77.2021},
    {id: 'CAM_04', lat: 28.6250, lng: 77.2000},
    {id: 'CAM_05', lat: 28.6350, lng: 77.2300}
];"""

new_cameras = """const CAMERAS = [
    {id: 'CAM_01', lat: 28.6315, lng: 77.2167},
    {id: 'CAM_02', lat: 28.6258, lng: 77.2343},
    {id: 'CAM_03', lat: 28.6129, lng: 77.2295}
];"""

content = content.replace(old_cameras, new_cameras)

with open("geofence.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated CAMERAS coordinates successfully!")
